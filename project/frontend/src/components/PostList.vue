<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { postStore } from '../stores/posts'
import { graphStore } from '../stores/graph'
import LoadingIcon from './icons/Loading.vue'
import UserTab from './UserTab.vue'
import PostSummary from './PostSummary.vue'

</script>

<script>
const FILENAME = "PostList"

export default {
  async beforeMount() {
    console.log(FILENAME, "beforeMount", "start");
    //console.log("PostList", this.postList);
    console.log(FILENAME, "beforeMount", this.postList.length);
    console.log(FILENAME, "beforeMount", "end");
  },
  props: ['postList', 'showCreatorStats', 'showIfHidden'],
  data() {
    return {
      loading: false,
    }
  },
  computed: {},
  methods: {
    ...mapActions(graphStore, { getFeed: 'getFeed', follow: 'follow', unfollow: 'unfollow' }),

    async followersUpdate(operation, user_id) {
      console.log(FILENAME, "followersUpdate", "start");
      console.log(FILENAME, "followersUpdate", operation, user_id);

      this.loading = true;

      let res = null;
      if (operation == '+') {
        res = await this.follow(user_id);
      } else {
        res = await this.unfollow(user_id);
      }

      if (res == null) {
        this.loading = false;
        console.log(FILENAME, "followersUpdate", "res is null");
        return;
      }

      // console.log(this.postList.posts);
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
      console.log(FILENAME, "followersUpdate", "end");
    },
  }
}
</script>

<template>
  <div class="px-3 mt-2">
    <div>
      <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
    </div>
    <div class="col-md-10 offset-md-1">
      <template v-if="postList.length > 0">
        <table class="table">
          <tbody>
            <tr v-for="(post) in postList" :key="post.post_id">
              <td :class="{ 'bg-danger': (showIfHidden && post.hidden) }">
                <PostSummary :postData="post" :showCreatorStats="showCreatorStats" :followersUpdate="followersUpdate" />
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
</template>

<style scoped>
</style>
