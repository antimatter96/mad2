<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { graphStore } from '../../stores/graph'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserSummary from '../../components/UserSummary.vue'

</script>

<script>
const FILENAME = "UserSearch";

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start")

    await this.checkUserState(this);

    console.log(FILENAME, "beforeMount", "end")
    this.loading = false;
  },

  data() {
    return {
      loading: true,
      userList: [],
      mode: '',
      searchText: "",
      searching: false,
    }
  },

  methods: {
    ...mapActions(graphStore, {
      getList: 'getList', searchByPrefix: 'searchByPrefix', follow: 'follow', unfollow: 'unfollow'
    }),
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),

    followersUpdate(a, b) {
      console.log("parent", a, b, followersUpdate);
    },

    async search() {
      this.loading = true;
      console.log(FILENAME, "search", "start")

      console.log(FILENAME, "search", "searchText", this.searchText);
      this.searchText = this.searchText.trim();
      console.log(FILENAME, "search", "searchText trimmed", this.searchText);

      if (this.searchText != "") {
        this.searching = true;
        this.userList = [];

        this.userList = await this.searchByPrefix(this.searchText);

        console.log(this.userList);
      }

      console.log(FILENAME, "search", "end")
      this.loading = false;
    },

    async followersUpdate(operation, user_id) {
      this.loading = true;
      console.log(FILENAME, "followersUpdate", "start")

      console.log(FILENAME, "followersUpdate", { operation, user_id })

      let action = operation == '+' ? this.follow : this.unfollow;

      let res = await action(user_id);
      if (res == null) {
        this.loading = false;
        return;
      }

      for (let i = 0; i < this.userList.users.length; i++) {
        if (user_id == this.userList.users[i].user_id) {

          if (operation == '+') {
            this.userList.users[i].user_follows = true;
          } else {
            this.userList.users[i].user_follows = false;
          }

          console.log(this.userList.users[i]);
          break;
        }
      }

      console.log(FILENAME, "followersUpdate", "end")
      this.loading = false;
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
      <div>
        <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
      </div>
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
            <tr v-for="(user, index) in userList.users" :key="user.user_id">
              <td class="small-index"> {{ index + 1 }} </td>
              <td>
                <UserSummary :showSummary="true" :userData="user" :showFollowing="true" :showFollowers="true"
                  class="d-flex align-items-center" @followAction="followersUpdate" />
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
