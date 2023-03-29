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

    // console.log(this.postList.posts);
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
        console.log("res is null");
        return;
      }

      console.log(this.postList.posts);
      for (let i = 0; i < this.postList.posts.length; i++) {
        if (user_id == this.postList.posts[i].creator.user_id) {
          if (operation == '+') {
            this.postList.posts[i].creator.user_follows = true;
          } else {
            this.postList.posts[i].creator.user_follows = false;
          }
        }
      }

      this.loading = false;
      console.log(res);
    },

  }
}
</script>

<template>
  <div v-if="postList == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else class="px-3">
    <div class="col-md-10 offset-md-1 mt-2 border-bottom border-2">
      <h3 class="mb-3 text-center">
        Your Feed
      </h3>
    </div>
    <div class="mt-2">
      <div>
        <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
      </div>
      <div class="col-md-10 offset-md-1">
        <template v-if="postList.count > 0">
          <table class="table">
            <tbody>
              <tr v-for="(post) in postList.posts" :key="post.post_id">
                <td>
                  <PostSummary :postData="post" :showCreatorStats="true" :followersUpdate="followersUpdate"/>
                </td>
              </tr>
            </tbody>
          </table>
        </template>
        <template v-else>
          <h4 class="text-center text-info">
            You don't follow anyone yet <br>
            People who you follow haven't created any posts <br>
          </h4>
        </template>

      </div>
    </div>

  </div>
</template>

<style scoped>
</style>
