<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { graphStore } from '../../stores/graph'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserSummary from '../../components/UserSummary.vue'
import PostList from '../../components/PostList.vue'
</script>

<script>
const FILENAME = "UserProfile"

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start")

    await this.checkUserState(this);

    console.log(FILENAME, "beforeMount", "this.$route.params", this.$route.params);

    this.username = this.$route.params.username;

    this.userData = await this.getUserInfo(this.username);

    this.userData.posts.count = this.userData.posts.length;
    this.isActuallyUser = this.userData['is_actually_user'];

    console.log(FILENAME, "beforeMount", "end");
    this.loading = false;
  },

  data() {
    return {
      loading: true,
      userData: null,
      username: '',
    }
  },

  methods: {
    ...mapActions(graphStore, { getUserInfo: 'getUserInfo', follow: 'follow', unfollow: 'unfollow' }),
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

      if (operation == '+') {
        this.userData.followers.length++;
        this.userData.user_follows = true;
      } else {
        this.userData.followers.length--;
        this.userData.user_follows = false;
      }

      console.log(FILENAME, "followersUpdate", "end");
      this.loading = false;
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
      <div class="d-flex align-items-center mb-4 text-center justify-content-center border-bottom pb-2">
        <h1 class="mb-0"> {{ userData.name || userData.email }} </h1>
        <UserSummary v-if="!isActuallyUser" :showSummary="false" :userData="userData" :showFollowing="true"
          :showFollowers="true" @followAction="followersUpdate" />
      </div>
      <div class="d-flex px-4 text-center justify-content-between">
        <div v-if="isActuallyUser" class="w-30">
          <RouterLink to="/profile/me/followers" class="fw-bold text-decoration-none">
            <h5>Followers</h5>
            <h5>{{ userData.followers.length }}</h5>
          </RouterLink>
        </div>
        <div v-else class="w-30">
          <h5>Followers</h5>
          <h5>{{ userData.followers.length }}</h5>
        </div>

        <div v-if="isActuallyUser" class="w-30">
          <RouterLink to="/profile/me/following" class="fw-bold text-decoration-none">
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
        <RouterLink to="/profile/me/export" class="fw-bold btn border border-info">
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
