<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { graphStore } from '../stores/graph'
import LoadingIcon from '../components/icons/Loading.vue'

import UserTab from '../components/UserTab.vue'

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

    console.log("this.userList", this.userList);


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

    async followersUpdate(operation, user_id) {
      this.loading = true;

      console.log("parent", operation, user_id, "followersUpdate");

      let res = null;
      if (operation == '+') {
        res = await this.follow(user_id);
      } else {
        res = await this.unfollow(user_id);
      }

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
      this.loading = false;
      console.log(res);
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
                  <UserTab :showSummary="true" :userData="user" :showFollowing="true" :showFollowers="showingFollowing"
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
