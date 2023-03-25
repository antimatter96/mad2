<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import Navigation from './components/Navigation.vue'
import { userAuthStore } from './stores/userAuth'
import LoadingIcon from './components/icons/Loading.vue'

</script>

<script>
export default {
  // 
  created() {
    console.log("App.vue", "CREATED START")
    console.log("App.vue", "CREATED END")
  },
  async beforeMount() {
    console.log("App.vue", "BEFORE MOUNTED START")

    this.loading = true;
    console.log("DONE async");

    console.log("loggedin", this.loggedIn)
    if (!this.loggedIn) {
      await this.checkUserState();
    }

    if (!this.loggedIn) {
      await this.checkUserState();

      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/login');
      this.loading = false;
    }

    this.loading = false;
    console.log("App.vue", "BEFORE MOUNTED END")
  },
  async mounted() {

  },
  // 
  data() {
    return {
      loading: true,
    }
  },
  // 
  computed: {
    ...mapState(userAuthStore, { loggedIn: 'loggedIn' }),
    hideNavBar() {
      return this.loading
    },
  },
  methods: {
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),
  }
}
</script>

<template>
  <div class="container d-flex flex-column px-4">
    <Navigation :loggedIn=loggedIn :loading=hideNavBar />

    <div id="main" class="row py-2">
      <div v-if="loading" id="main-loading" class="h-100 w-100">
        <LoadingIcon element="h2" />
      </div>
      <div v-else>
        <RouterView />
      </div>
    </div>


    <footer class="row pt-4 pb-4 mt-auto ">
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
