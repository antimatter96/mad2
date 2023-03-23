<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { apiStore } from '../stores/api'
import LoadingIcon from './icons/Loading.vue'

import UserTab from './UserTab.vue'

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

    console.log(this.$route);


    this.mode = this.$route.name;
    this.showingFollowers = this.mode == 'user_followers';

    if (!this.loggedIn) {
      await this.checkUserState()
    }
    if (!this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/login');
      this.loading = false;
    }
    console.log("App.vue", "BEFORE MOUNTED END")

    console.log("mode", this.mode);
    this.userList = await this.getList(this.showingFollowers);


    this.loading = false;
  },
  async mounted() {
  },
  // 
  data() {
    return {
      msg: "U did it",
      loading: true,
      userList: null,
      mode: '',
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
    ...mapActions(apiStore, { getList: 'getList' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),
  }
}
</script>

<template>
  <div v-if="loading || userList == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else>
    <div class="col-md-4 py-4"></div>
    <div class="px-1">
      <h3 class="mb-0">
        <span v-if="showingFollowers"> Your Followers : </span>
        <span v-else>Who you follow : </span>
        ({{ userList.length }})
      </h3>
      <div>
        <h5> List </h5>
      <template v-for="(user, index) in userList.list" class="bg-red">
        <span> {{index+1}} </span> <UserTab :userData="user" />
      </template>
    </div>
    </div>
  </div>
</template>

<style scoped>
</style>
