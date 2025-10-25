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
  <div class="circular-timer">
    <svg width="60" height="60">
      <circle cx="30" cy="30" r="28" stroke="#eee" stroke-width="4" fill="none" />
      <circle
        cx="30" cy="30" r="28"
        :stroke="active ? '#007bff' : '#aaa'"
        stroke-width="4"
        fill="none"
        :stroke-dasharray="2 * Math.PI * 28"
        :stroke-dashoffset="(2 * Math.PI * 28) * (1 - percent / 100)"
        stroke-linecap="round"
        style="transition: stroke-dashoffset 0.5s linear;"
      />
      <text x="30" y="36" text-anchor="middle" font-size="18" fill="#333">{{ timeLeft }}</text>
    </svg>
  </div>
</template>

<style scoped>
.circular-timer {
  display: inline-block;
  width: 60px;
  height: 60px;
}
</style>
