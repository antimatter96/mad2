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
    this.showingFollowing = this.mode != 'user_followers';

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
    this.userList = [];

    this.loading = false;
  },
  async mounted() {
  },
  // 
  data() {
    return {
      loading: true,
      userList: null,
      mode: '',
      searchText: null,
      searching: false,
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
    ...mapActions(apiStore, { getList: 'getList', searchByPrefix: 'searchByPrefix' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    followersUpdate(a, b) {
      console.log(parent, a, b);
    },

    async search() {
      console.log(this.searchText, "<<<<<<<<<<")

      this.userList = await this.searchByPrefix(this.searchText);

      console.log(this.userList);

    }
  }
}
</script>

<template>
  <div v-if="loading || userList == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else class="px-3">
    <div class="col-md-10 offset-md-1 border-bottom border-2">
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Recipient's username" v-model="searchText">
        <button class="btn btn-primary" type="button" v-on:click="search">Button</button>
      </div>
    </div>
    <div class="mt-4">
      <div v-if="userList.count > 0" class="col-md-10 offset-md-1">
        <h5> Search Result </h5>
        <div v-for="(user, index) in userList.users">
          <span> {{ index + 1 }} </span>
          <UserTab :showSummary="true" :userData="user" :showFollowing="true" :showFollowers="showingFollowing"
            class="d-flex" />
        </div>
      </div>
      <div v-else-if="searching == true" class="col-md-10 offset-md-1">
        Nothing Found
      </div>
      <div v-else class="col-md-10 offset-md-1">
        Start Searching
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
