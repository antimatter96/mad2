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
  <header class="row w-100 m-0 mb-4">
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
                <RouterLink replace to="/" class="nav-link">Home</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink replace to="/profile/me" class="nav-link">My Profile</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink :to="{ name: 'user_search_page' }" class="nav-link">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search"
                    viewBox="0 0 16 16">
                    <path
                      d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                  </svg> Search
                </RouterLink>
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
  </header>
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
