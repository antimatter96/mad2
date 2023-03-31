<script setup>
import { RouterLink } from 'vue-router';
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'

import Loading from './icons/Loading.vue';
</script>

<script>
export default {
  props: ['loggedIn', 'loading'],
  async mounted() {
    console.log(this.loggedIn)
  },
  methods: {
    ...mapActions(userAuthStore, { logout: 'logout' }),

    async _logout() {
      console.log("parent", "_logout");
      let logoutUser = confirm("Do you want to logout ?");
      if (logoutUser) {
        this.logout();
        this.$router.push({
          name: 'login'
        });
      }
    }
  }
}
</script>

<template>
  <header class="row w-100 m-0 mb-4">
    <nav class="navbar navbar-expand-lg navbar-light border-bottom mb-1 px-0 py-1">
      <div class="container-fluid px-0">

        <RouterLink to="/" class="navbar-brand py-0">
          <h1 class="mb-0 text-warning">microBlog</h1>
        </RouterLink>

        <div class="collapse navbar-collapse" id="navbarColor03">
          <ul class="navbar-nav ms-auto">
            <div v-if="loading">
              <Loading element="h4" />
            </div>
            <template v-else-if="loggedIn">
              <li class="nav-item fw-bolder">
                <RouterLink replace to="/" class="nav-link">Home</RouterLink>
              </li>
              <li class="nav-item nav-item-btn">
                <RouterLink :to="{ name: 'newPost' }" class="btn btn-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                    class="bi bi-file-earmark-plus" viewBox="0 0 16 16">
                    <path
                      d="M8 6.5a.5.5 0 0 1 .5.5v1.5H10a.5.5 0 0 1 0 1H8.5V11a.5.5 0 0 1-1 0V9.5H6a.5.5 0 0 1 0-1h1.5V7a.5.5 0 0 1 .5-.5z" />
                    <path
                      d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z" />
                  </svg> New Post
                </RouterLink>
              </li>
              <li class="nav-item fw-bolder">
                <RouterLink replace to="/profile/me" class="nav-link">My Profile</RouterLink>
              </li>
              <li class="nav-item fw-bolder">
                <RouterLink :to="{ name: 'user_search_page' }" class="nav-link">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search"
                    viewBox="0 0 16 16">
                    <path
                      d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                  </svg> Search
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
</style>
