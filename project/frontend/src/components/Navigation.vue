<script setup>
import { RouterLink } from 'vue-router';
import { mapActions } from 'pinia'

import { userAuthStore } from '../stores/userAuth'

import Loading from './icons/Loading.vue';
import NewPostIcon from './icons/Search.vue';
import SearchIcon from './icons/NewPost.vue';
</script>

<script>
const FILENAME = "Navigation";

export default {
  async mounted() {
    console.log(FILENAME, "mounted")
  },

  props: ['loggedIn', 'loading'],

  methods: {
    ...mapActions(userAuthStore, { logout: 'logout' }),

    async _logout() {
      console.log(FILENAME, "_logout", "start");

      let logoutUser = window.confirm("Do you want to logout ?");
      if (!logoutUser) {
        console.log(FILENAME, "_logout", "abandoned");
        return
      }

      this.logout();
      this.$router.push({ name: 'login' });

      console.log(FILENAME, "_logout", "end");
    }
  }
}
</script>

<template>
  <header class="row w-100 m-0 mb-4">
    <nav class="navbar navbar-expand-lg navbar-light border-bottom mb-1 px-0 py-1">
      <div class="container-fluid px-0">

        <RouterLink to="/" class="navbar-brand py-0">
          <h1 class="mb-0 text-warning main-heading">microBlog</h1>
        </RouterLink>

        <div class="collapse navbar-collapse" id="navbarColor03">
          <ul class="navbar-nav ms-auto">
            <div v-if="loading">
              <Loading element="h4" />
            </div>
            <template v-else-if="loggedIn">
              <li class="nav-item fw-bolder">
                <RouterLink to="/" class="nav-link">Home</RouterLink>
              </li>
              <li class="nav-item nav-item-btn">
                <RouterLink :to="{ name: 'newPost' }" class="btn btn-primary">
                  <SearchIcon /> New Post
                </RouterLink>
              </li>
              <li class="nav-item fw-bolder">
                <RouterLink to="/profile/me" class="nav-link">My Profile</RouterLink>
              </li>
              <li class="nav-item fw-bolder">
                <RouterLink :to="{ name: 'user_search_page' }" class="nav-link">
                  <NewPostIcon /> Search
                </RouterLink>
              </li>
              <li class="nav-item nav-item-btn">
                <a class="btn btn-danger" v-on:click="_logout">Logout</a>
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

.main-heading {
  text-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
}
</style>
