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
    ...mapActions(graphStore, {
      getList: 'getList', searchByPrefix: 'searchByPrefix', follow: 'follow', unfollow: 'unfollow'
    }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    followersUpdate(a, b) {
      console.log("parent", a, b, followersUpdate);
    },

    async search() {
      this.loading = true;
      this.searching = true;
      this.userList = [];
      console.log(this.searchText, "<<<<<<<<<<")

      this.userList = await this.searchByPrefix(this.searchText);

      this.loading = false;

      console.log(this.userList);
    },
  }
}
</script>

<template>

  <div class="px-3">
    <div class="col-md-10 offset-md-1 border-bottom border-2">
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Enter username" v-model="searchText">
        <button class="btn btn-primary w-15" type="button" v-on:click="search">Search</button>
      </div>
    </div>
    <div class="mt-2">
      <div><LoadingIcon :element="'h4'" element="h4" :style="{'opacity': (loading? 100: 0)}"></LoadingIcon></div>
      <div v-if="userList.count > 0" class="col-md-10 offset-md-1">
        <h5> Search Result </h5>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in userList.users" class="">
              <td class="small-index"> {{ index + 1 }} </td>
              <td>
                <UserTab :showSummary="true" :userData="user" :showFollowing="true" :showFollowers="showingFollowing"
                  class="d-flex align-items-center" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="loading == true" class="col-md-10 offset-md-1">
      </div>
      <div v-else-if="loading == false && searching == true" class="col-md-10 offset-md-1 text-center text-danger">
        <h4>Nothing Found</h4>
      </div>
      <div v-else class="col-md-10 offset-md-1 text-center">
        Start Searching
      </div>
    </div>
  </div>
</template>

<style scoped>
.small-index {
  vertical-align: middle;
}
</style>
