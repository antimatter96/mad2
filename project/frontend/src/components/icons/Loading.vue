<script setup>
defineProps({
  element: {
    type: String,
    required: true,
    value: "h1",
  },
  text: {
    type: String,
    required: false,
    value: "loading",
  },
})
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div class="loader mx-1">
      <h1 data-text="Loading..." v-if="element == 'h1'" class="loader_heading">Loading...</h1>
      <h2 data-text="Loading..." v-if="element == 'h2'" class="loader_heading">Loading...</h2>
      <h3 data-text="Loading..." v-if="element == 'h3'" class="loader_heading">Loading...</h3>
      <h4 data-text="Loading..." v-if="element == 'h4'" class="loader_heading">Loading...</h4>
      <h5 data-text="Loading..." v-if="element == 'h5'" class="loader_heading">Loading...</h5>
      <h6 data-text="Loading..." v-if="element == 'h6'" class="loader_heading">Loading...</h6>
    </div>
  </div>
</template>

<style scoped>
.loader_heading:before {
  content: attr(data-text);
  position: absolute;
  overflow: hidden;
  max-width: 7em;
  white-space: nowrap;
  color: #4582ec;

  animation-name: loading;
  animation-duration: 2s;
  animation-timing-function: cubic-bezier(0.895, 0.03, 0.685, 0.22);
  animation-iteration-count: infinite;
}

@keyframes loading {
  0% {
    max-width: 0;
  }
}

.loader {
  text-align: center;
}

.loader_heading {
  margin-bottom: 0px;
}
</style>
