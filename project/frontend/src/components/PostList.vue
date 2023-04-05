<script setup>
import { mapActions, mapState } from 'pinia'

import { graphStore } from '../stores/graph'

import LoadingIcon from './icons/Loading.vue'
import PostSummary from './PostSummary.vue'
</script>

<script>
const FILENAME = "PostList";

export default {
  async beforeMount() {
    console.log(FILENAME, "beforeMount", "start");
    console.log(FILENAME, "beforeMount", this.postList.length);
    console.log(FILENAME, "beforeMount", "end");
  },

  props: ['postList', 'showCreatorStats', 'showIfHidden', 'followAction'],

  data() {
    return {
      loading: false,
    }
  },

  methods: {
    ...mapActions(graphStore, { getFeed: 'getFeed', follow: 'follow', unfollow: 'unfollow' }),

    async followersUpdate(operation, user_id) {
      this.loading = true;
      console.log(FILENAME, "followersUpdate", "start");

      console.log(FILENAME, "followersUpdate", operation, user_id);

      let action = operation == '+' ? this.follow : this.unfollow;

      let res = await action(user_id);
      if (res == null) {
        this.loading = false;
        console.log(FILENAME, "followersUpdate", "res is null");
        return;
      }

      for (let i = 0; i < this.postList.length; i++) {
        if (user_id == this.postList[i].creator.user_id) {
          if (operation == '+') {
            this.postList[i].creator.user_follows = true;
          } else {
            this.postList[i].creator.user_follows = false;
          }
          break;
        }
      }

      this.$emit("followAction", operation, user_id);

      console.log(FILENAME, "followersUpdate", "end");
      this.loading = false;
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
      <table class="table">
        <tbody>
          <tr v-for="(post) in postList" :key="post.post_id"
            :class="{ 'border-danger border-2 border my-1': (showIfHidden && post.hidden) }">
            <td>
              <span class="text-danger fw-bold" v-if="showIfHidden && post.hidden">Hidden</span>
              <PostSummary :postData="post" :showCreatorStats="showCreatorStats" :followersUpdate="followersUpdate" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
</style>
