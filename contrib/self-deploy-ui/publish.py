#!/usr/bin/env python3
"""Publish a ready UI build from this VPS's Woodpecker agent."""
import fcntl
import json
import os
import re
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path, PurePosixPath

STATE = Path("/opt/woodpecker-ci")
DB = Path("/var/lib/docker/volumes/woodpecker_server-data/_data/woodpecker.sqlite")
SITE = Path("/srv/edge/sites/woodpecker-ui")
ORIGIN = "https://ci.getdiff.ru"
REPO = "shawniwe/woodpecker"
BRANCH = "experiment/shadcn-self-deploy"
ARCHIVE = "/tmp/woodpecker-ui.tar.gz"
READY = "/tmp/woodpecker-ui.ready"
RECEIVED = "/tmp/woodpecker-ui.received"
FAILED = "/tmp/woodpecker-ui.failed"


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, capture_output=True, timeout=20, **kwargs).stdout


def get_ready_run():
    with sqlite3.connect(f"file:{DB}?mode=ro", uri=True) as db:
        return db.execute(
            """
            SELECT p.number, p."commit"
            FROM pipelines p JOIN repos r ON r.id = p.repo_id
            WHERE r.full_name = ? AND p.branch = ? AND p.event = 'manual'
              AND p.status = 'running'
              AND EXISTS (
                SELECT 1 FROM steps s
                WHERE s.pipeline_id = p.id AND s.name = 'build' AND s.state = 'success'
              )
              AND EXISTS (
                SELECT 1 FROM steps s
                WHERE s.pipeline_id = p.id AND s.name = 'handoff-ui' AND s.state = 'running'
              )
            ORDER BY p.number DESC LIMIT 1
            """,
            (REPO, BRANCH),
        ).fetchone()


def find_container(number, revision):
    expected = {f"CI_REPO={REPO}", f"CI_PIPELINE_NUMBER={number}", f"CI_COMMIT_SHA={revision}"}
    for container in run("docker", "ps", "-q", "--filter", "label=wp_step=handoff-ui").split():
        env = json.loads(run("docker", "inspect", "--format", "{{json .Config.Env}}", container))
        if expected <= set(env):
            ready = subprocess.run(
                ("docker", "exec", container, "sh", "-c",
                 f"test -f {READY} && ! test -f {RECEIVED} && ! test -f {FAILED}"),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10,
            )
            if ready.returncode == 0:
                return container
    return None


def stage_release(container, revision, scratch):
    archive_path = scratch / "ui.tar.gz"
    prefix = PurePosixPath("assets", "fork-ui", revision)
    run("docker", "cp", f"{container}:{ARCHIVE}", str(archive_path))
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        if sum(member.size for member in members) > 100 * 1024**2 or len(members) > 3000:
            raise ValueError("UI archive exceeds the expected size")
        for member in members:
            name = PurePosixPath(member.name)
            if (".." in name.parts or not (member.isdir() or member.isfile())
                    or not (name == PurePosixPath("index.html") or name.is_relative_to(prefix))):
                raise ValueError(f"Unexpected archive entry: {member.name}")
        archive.extractall(scratch, filter="data")
    html = (scratch / "index.html").read_text()
    scripts = re.findall(r'<script[^>]+src="(/assets/fork-ui/[^"]+\.js)"', html)
    if len(scripts) != 1 or not scripts[0].startswith(f"/{prefix}/"):
        raise ValueError("The UI entry point does not match the build revision")
    staged = scratch / prefix
    shutil.copyfile(scratch / "index.html", staged / "index.html")
    for path in [staged, *staged.rglob("*")]:
        path.chmod(0o755 if path.is_dir() else 0o644)

    release = SITE / "releases" / revision
    if release.exists():
        # The asset URLs are immutable for each commit.
        for path in staged.iterdir():
            if not (release / path.name).is_file() or path.read_bytes() != (release / path.name).read_bytes():
                raise ValueError("A release already exists with different files for this commit")
    else:
        staged.rename(release)
    return scripts[0]


def set_current(target, scratch):
    current = SITE / "current"
    if target is None:
        current.unlink(missing_ok=True)
    else:
        link = scratch / "current"
        link.symlink_to(target)
        os.replace(link, current)


def http(path, *args):
    return run("curl", "-fsS", "--max-time", "4",
               "--resolve", "ci.getdiff.ru:443:127.0.0.1", *args, f"{ORIGIN}{path}")


def verify(asset):
    for attempt in range(5):
        try:
            if (all(asset in http(route) for route in ("/", "/repos", "/admin", "/login", "/repos/4/pipeline/4"))
                    and http("/api/healthz", "-o", "/dev/null", "-w", "%{http_code}") == "204"):
                http(asset, "-o", "/dev/null")
                return
        except subprocess.SubprocessError:
            pass
        if attempt < 4:
            time.sleep(1)
    raise RuntimeError("Published UI failed the HTTPS check")


def publish(container, number, revision):
    releases = SITE / "releases"
    releases.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".deploy-", dir=releases) as directory:
        scratch = Path(directory)
        asset = stage_release(container, revision, scratch)
        current = SITE / "current"
        previous = os.readlink(current) if current.is_symlink() else None
        set_current(f"releases/{revision}", scratch)
        try:
            verify(asset)
            run("docker", "exec", container, "touch", RECEIVED)
        except Exception:
            set_current(previous, scratch)
            raise
    print(f"Published Woodpecker UI from pipeline #{number}: {revision}", flush=True)


def main():
    with (STATE / "publish-ui.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ready = get_ready_run()
        if not ready:
            return
        number, revision = ready
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Invalid commit SHA")
        container = find_container(number, revision)
        if not container:
            return
        try:
            publish(container, number, revision)
        except Exception as error:
            print(f"Pipeline #{number} UI publication failed: {error}", flush=True)
            run("docker", "exec", container, "touch", FAILED)
            raise


if __name__ == "__main__":
    main()
