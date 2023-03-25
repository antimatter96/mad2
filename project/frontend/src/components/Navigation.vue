<script setup>
import { RouterLink } from 'vue-router';
import Loading from './icons/Loading.vue';
</script>

<script>
export default {
  props: ['loggedIn', 'loading'],
  async mounted() {
    console.log(this.loggedIn)
  },
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light border-bottom mb-1 px-0 py-1">
    <div class="container-fluid px-0">

      <RouterLink to="/" class="navbar-brand py-0">
        <h1 class="mb-0">microBlog</h1>
      </RouterLink>

      <div class="collapse navbar-collapse" id="navbarColor03">
        <ul class="navbar-nav ms-auto">
          <div v-if="loading">
            <Loading element="h4" />
          </div>
          <template v-else-if="loggedIn">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/profile/me" class="nav-link">My Profile</RouterLink>
            </li>
            <li class="nav-item nav-item-btn">
              <RouterLink to="/logout" class="btn btn-danger">Logout</RouterLink>
            </li>
          </template>
          <template v-else>
            <li class="nav-item nav-item-btn">
              <RouterLink to="/login" class="btn btn-primary">Login</RouterLink>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav-item {
  border-bottom: 1px solid black;
  margin-left: 4px;
}

.nav-item-btn {
  border-bottom: 1px solid transparent;
  margin-left: 4px;
}
</style>
