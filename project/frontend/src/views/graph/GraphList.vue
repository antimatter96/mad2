<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { graphStore } from '../../stores/graph'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserSummary from '../../components/UserSummary.vue'
</script>

<script>
const FILENAME = "GraphList";

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start");

    await this.checkUserState(this);

    console.log(this.$route);

    this.mode = this.$route.name;
    this.showingFollowers = this.mode == 'user_followers';
    this.showingFollowing = this.mode != 'user_followers';

    console.log("mode", this.mode);

    this.userList = await this.getList(this.showingFollowers);

    console.log("this.userList", this.userList);

    console.log(FILENAME, "beforeMount", "end");
    this.loading = false;
  },

  data() {
    return {
      loading: true,
      userList: null,
      mode: '',
    }
  },

  methods: {
    ...mapActions(graphStore, { getList: 'getList', follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),

    async followersUpdate(operation, user_id) {
      this.loading = true;
      console.log(FILENAME, "followersUpdate", "start");

      console.log(FILENAME, "followersUpdate", { operation, user_id });

      let action = operation == '+' ? this.follow : this.unfollow;

      let res = await action(user_id);
      if (res == null) {
        this.loading = false;
        return;
      }

      console.log(this.userList);
      for (let i = 0; i < this.userList.list.length; i++) {
        if (user_id == this.userList.list[i].user_id) {

          if (operation == '+') {
            this.userList.list[i].user_follows = true;
          } else {
            this.userList.list[i].user_follows = false;
          }

          console.log(this.userList.list[i]);

          if (this.showingFollowers) {

          }
          if (this.showingFollowing) {
            if (operation == '-') {
              this.userList.length--;
              this.userList.list.splice(i, 1);

            } else {
              this.userList.length++;
            }
          }

          break;
        }
      }

      console.log(FILENAME, "followersUpdate", "end");
      this.loading = false;
    },
  }

}
</script>

<template>
  <div v-if="userList == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else class="px-3">
    <div class="col-md-10 offset-md-1 mt-2 border-bottom border-2">
      <h3 class="mb-3 text-center">
        <span v-if="showingFollowers"> Your Followers : </span>
        <span v-else>Who you follow : </span> ({{ userList.length }})
      </h3>
    </div>
    <div class="mt-2">
      <div>
        <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
      </div>
      <div class="col-md-10 offset-md-1">
        <template v-if="userList.length > 0">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in userList.list" class="">
                <td class="small-index"> {{ index + 1 }} </td>
                <td>
                  <UserSummary :showSummary="true" :userData="user" :showFollowing="true" :showFollowers="showingFollowing"
                    @followAction="followersUpdate" class="d-flex align-items-center" />
                </td>
              </tr>
            </tbody>
          </table>
        </template>
        <template v-else>
          <h4 class="text-center text-danger">
            <span v-if="showingFollowers"> No one follows you yet :/ : </span>
            <span v-else>You don't follow anyone yet </span>
          </h4>
        </template>

      </div>
    </div>

  </div>
</template>

<style scoped>
.small-index {
  vertical-align: middle;
}
</style>
