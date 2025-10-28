<script setup>
import { computed } from 'vue';
const props = defineProps({
  timeLeft: Number,
  duration: Number,
  active: Boolean,
});

const percent = computed(() => (props.timeLeft / props.duration) * 100);
</script>

<template>
  <div class="inline-block relative w-16 h-16">
    <svg viewBox="0 0 60 60" class="w-full h-full">
      <circle cx="30" cy="30" r="28" stroke="#e5e7eb" stroke-width="4" fill="none" />
      <circle
        cx="30" cy="30" r="28"
        :stroke="active ? '#8b5cf6' : '#aaa'"
        stroke-width="4"
        fill="none"
        :stroke-dasharray="2 * Math.PI * 28"
        :stroke-dashoffset="(2 * Math.PI * 28) * (1 - percent / 100)"
        stroke-linecap="round"
        class="transition-all duration-500"
      />
      <text x="30" y="36" text-anchor="middle" font-size="16" :fill="active ? '#8b5cf6' : '#555'" class="font-semibold">
        {{ timeLeft }}
      </text>
    </svg>
    <div v-if="active" class="absolute inset-0 rounded-full ring-2 ring-main-violet ring-opacity-40 animate-pulse"
    ></div>
  </div>
</template>

