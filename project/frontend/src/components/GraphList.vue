<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { graphStore } from '../stores/graph'
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
    this.userList = await this.getList(this.showingFollowers);

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
    ...mapActions(graphStore, { getList: 'getList', follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    async followersUpdate(mode, user_id) {
      console.log("parent", mode, user_id, "followersUpdate");

      let res = null;
      if (mode == '+') {
         res = await this.follow(user_id);
      } else {
         res = await this.unfollow(user_id);
      }
      
      console.log(res);
    }
  }
}
</script>

<template>
  <div v-if="loading || userList == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else>
    <div class="px-1">
      <h3 class="mb-0">
        <span v-if="showingFollowers"> Your Followers : </span>
        <span v-else>Who you follow : </span>
        ({{ userList.length }})
      </h3>
      <div>
        <h5> List </h5>
        <div class="col-md-10 offset-md-1">
        <div v-for="(user, index) in userList.list">
          <span> {{ index + 1 }} </span>
          <UserTab :showSummary="true" :userData="user" :showFollowing="true" :showFollowers="showingFollowing" @followAction="followersUpdate"
          class="d-flex"/>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
