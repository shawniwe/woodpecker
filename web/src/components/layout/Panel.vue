<template>
  <Card class="w-full gap-0 overflow-hidden p-0 shadow-xs">
    <component
      :is="collapsable ? 'button' : 'div'"
      v-if="title"
      type="button"
      class="border-border bg-wp-background-200 text-card-foreground flex w-full items-center gap-2 border-b px-4 py-2.5 text-sm font-semibold"
      :aria-expanded="collapsable ? !collapsed : undefined"
      :class="{
        'cursor-pointer': collapsable,
      }"
      @click="_collapsed = !_collapsed"
    >
      <Icon
        v-if="collapsable"
        name="chevron-right"
        class="h-6 min-w-6 transition-transform duration-150"
        :class="{ 'rotate-90 transform': !collapsed }"
      />
      {{ title }}
    </component>
    <div
      :class="{
        'max-h-auto': !collapsed,
        'max-h-0': collapsed,
      }"
      class="transition-height overflow-hidden duration-150"
    >
      <div class="text-wp-text-100 w-full p-4">
        <slot />
      </div>
    </div>
  </Card>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';

import Icon from '~/components/atomic/Icon.vue';
import Card from '~/components/ui/card/Card.vue';

const props = defineProps<{
  title?: string;
  collapsable?: boolean;
  collapsedByDefault?: boolean;
}>();

/**
 * _collapsed is used to store the internal state of the panel, but is
 * ignored if the panel is not collapsable.
 */
const _collapsed = ref(props.collapsedByDefault || false);

const collapsed = computed(() => props.collapsable && _collapsed.value);
</script>
