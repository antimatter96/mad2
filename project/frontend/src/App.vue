<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import Navigation from './components/Navigation.vue'
import { userAuthStore } from './stores/userAuth'
import LoadingIcon from './components/icons/Loading.vue'
</script>

<script>
const FILENAME = "App";

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start")

    console.log(FILENAME, "loggedin", this.loggedIn)
    await this.checkUserState(this);

    console.log(FILENAME, "beforeMount", "end");
    this.loading = false;
  },

  data() {
    return {
      loading: true,
    }
  },

  computed: {
    ...mapState(userAuthStore, { loggedIn: 'loggedIn' }),
  },

  methods: {
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),
  }
}
</script>

<template>
  <div class="container d-flex flex-column px-4">
    <Navigation :loggedIn=loggedIn :loading=loading />


    <div id="main" class="row py-2">
      <div v-if="loading" id="main-loading" class="h-100 w-100">
        <LoadingIcon element="h2" />
      </div>
      <div v-else>
        <RouterView :key="$route.fullPath" />
      </div>
    </div>


    <footer class="row py-4 mt-auto w-85 mx-auto border-top border-2">
      <div class="d-flex flex-row justify-content-evenly">
        <div>
          Some part of footer
        </div>
        <div>
          Some part of footer
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
</style>
