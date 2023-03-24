<script setup>
import { RouterLink } from 'vue-router';
import Loading from './icons/Loading.vue';

defineProps({
  msg: {
    type: String,
    required: true
  },
  loggedin: {
    type: Boolean,
  },
  loading: {
    type: Boolean
  }
})
</script>

<script>
export default {
  props: ['msg', 'loggedin', 'loading'],
  data() {
    return {}
  },
}
</script>


<template>
  <nav class="navbar navbar-expand-lg navbar-light border-bottom mb-1 px-0 py-1">
    <div class="container-fluid px-0">
      <a class="navbar-brand py-0">
        <h1 class="mb-0">microBlog</h1>
      </a>
      <div class="collapse navbar-collapse" id="navbarColor03">
        <ul class="navbar-nav ms-auto">
          <div v-if="loading">
            <Loading element="h4"/>
          </div>
          <template v-else>
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/profile/me" class="nav-link">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/logout" class="btn btn-danger" v-if="loggedin">Logout</RouterLink>
              <RouterLink to="/login" class="btn btn-primary" v-if="!loggedin">Login</RouterLink>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>

</style>
