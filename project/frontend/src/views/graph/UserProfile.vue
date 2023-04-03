<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { graphStore } from '../../stores/graph'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserTab from '../../components/UserTab.vue'
import PostSummary from '../../components/PostSummary.vue'
import PostList from '../../components/PostList.vue'
</script>

<script>
const FILENAME = "UserProfile"

export default {
  async beforeMount() {
    console.log(FILENAME, "BEFORE MOUNTED START")
    this.loading = true;

    console.log("DONE async");

    console.log(this.$route);

    this.username = this.$route.params.username;

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

    this.userData = await this.getUserInfo(this.username);
    this.userData.posts.count = this.userData.posts.length;
    this.loading = false;

    this.isActuallyUser = this.userData['is_actually_user'];
  },
  async mounted() {
  },
  // 
  data() {
    return {
      loading: true,
      userData: null,
      username: '',
    }
  },
  // 
  computed: {
    ...mapState(userAuthStore, ['loggedIn']),
  },
  methods: {
    ...mapActions(graphStore, { getUserInfo: 'getUserInfo', follow: 'follow', unfollow: 'unfollow' }),
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


      if (operation == '+') {
        this.userData.followers.length++;
        this.userData.user_follows = true;
      } else {
        this.userData.followers.length--;
        this.userData.user_follows = false;
      }


      this.loading = false;
      console.log(res);
    },
  }
}
</script>

<template>
  <div v-if="userData == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else-if="Object.keys(userData).length > 0">
    <div>
      <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
    </div>
    <div class="px-3">
      <div>
        <h3 class="mb-0"> {{ userData.name || userData.email }} </h3>
        <UserTab v-if="!isActuallyUser" showSummary="false" :userData="userData" :showFollowing="true"
          :showFollowers="true" @followAction="followersUpdate" />
        <hr>
      </div>

      <div class="d-flex px-2 text-center">
        <div v-if="isActuallyUser" class="w-30">
          <RouterLink to="/profile/me/followers" replace class="fw-bold text-decoration-none">
            <h5>Followers</h5>
            <h5>{{ userData.followers.length }}</h5>
          </RouterLink>
        </div>
        <div v-else class="w-30">
          <h5>Followers</h5>
          <h5>{{ userData.followers.length }}</h5>
        </div>

        <div v-if="isActuallyUser" class="w-30">
          <RouterLink to="/profile/me/following" replace class="fw-bold text-decoration-none">
            <h5>Following</h5>
            <h5>{{ userData.following.length }}</h5>
          </RouterLink>
        </div>
        <div v-else class="w-30">
          <h5>Following</h5>
          <h5>{{ userData.following.length }}</h5>
        </div>
        <div class="w-30">
          <h5>Posts</h5>
          <h5>{{ userData.posts.length }}</h5>
        </div>
      </div>
    </div>

    <hr>
    <div class="px-3">
      <h3 class="text-center">Posts</h3>

      <h4 v-if="isActuallyUser" class="text-center">
        <RouterLink to="/profile/me/export" replace class="fw-bold btn">
          Export all posts data
        </RouterLink>
      </h4>

      <PostList :postList="userData.posts" :showCreatorStats="false" :showIfHidden="true" />
    </div>

  </div>
  <div v-else>
    <h3>
      Not Found
    </h3>
  </div>
</template>

<style scoped>
</style>
