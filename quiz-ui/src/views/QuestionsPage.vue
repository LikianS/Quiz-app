<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps(['question']);
defineEmits(['answer-clicked']);
</script>

<template>
  <div>
    <h2>{{ question.text }}</h2>
    <ul>
      <li v-for="(answer, index) in question.possibleAnswers" :key="index">
        <button @click="$emit('answer-clicked', index)">{{ answer }}</button>
      </li>
    </ul>
  </div>
</template>