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
      msg: "U did it",
      loading: true,
    }
  },
  // 
  computed: {
    ...mapState(userAuthStore, ['loggedIn']),
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
  <div class="container">
    <header class="row">
      <Navigation :msg=msg :loggedin=loggedin :loading=hideNavBar />
    </header>

    <div id="main" class="row py-2">
      <div v-if="loading" id="main-loading" class="h-100 w-100">
        <LoadingIcon element="h2" />
      </div>
      <div v-else>
        <RouterView />
      </div>
    </div>

    <footer class="row">
      Footer
    </footer>
  </div>
</template>

<style scoped>

</style>
