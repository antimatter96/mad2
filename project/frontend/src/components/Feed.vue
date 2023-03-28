<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { postStore } from '../stores/posts'
import { graphStore } from '../stores/graph'
import LoadingIcon from './icons/Loading.vue'
import UserTab from './UserTab.vue'
import PostSummary from './PostSummary.vue'

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

    console.log(this.$route, this.loggedIn);

    if (!this.loggedIn) {
      await this.checkUserState()
    }
    if (!this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/login');
      this.loading = false;

      return
    }
    console.log("App.vue", "BEFORE MOUNTED END")

    console.log("mode", this.mode);
    this.postList = await this.getFeed(0);

    this.loading = false;
  },
  async mounted() {
  },
  // 
  data() {
    return {
      loading: true,
      postList: null,
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
    ...mapActions(graphStore, { getFeed: 'getFeed', follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    followersUpdate(a, b) {
      console.log("parent", a, b, "followersUpdate");
    },
  }
}
</script>

<template>
  <div v-if="loading || postList == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else>

    <div class="col-md-4 py-4"></div>
    <div class="px-1">
      <h3 class="mb-0">
        <span> Your Feed : </span>
      </h3>
    </div>

    <div class="col-md-4 py-2"></div>

    <div class="col-md-10 offset-md-1">
      <div v-if="postList.count > 0">
        <template v-for="(post) in postList.posts" :key="post.post_id">
          <PostSummary :postData="post" :showCreatorStats="true"/>
        </template>
      </div>
      <div v-else>
        Nothing Found
      </div>
    </div>
    <div class="col-md-4 py-2"></div>
  </div>
</template>

<style scoped>
</style>
