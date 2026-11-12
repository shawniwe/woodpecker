<template>
  <component
    :is="to ? 'router-link' : clickable ? 'button' : 'div'"
    :to="to"
    class="border-border bg-card flex w-full overflow-hidden rounded-lg border p-4 shadow-xs"
    :class="{
      'hover:bg-wp-control-neutral-100 focus-visible:outline-wp-link-100 cursor-pointer transition-colors focus-visible:outline-2 focus-visible:-outline-offset-2':
        clickable || to,
    }"
  >
    <slot />
  </component>
</template>

<script lang="ts" setup>
import type { RouteLocationRaw } from 'vue-router';

defineProps<{
  clickable?: boolean;
  to?: RouteLocationRaw;
}>();
</script>
