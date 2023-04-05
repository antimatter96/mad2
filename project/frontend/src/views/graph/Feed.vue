<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { graphStore } from '../../stores/graph'

import LoadingIcon from '../../components/icons/Loading.vue'
import PostList from '../../components/PostList.vue'
</script>

<script>
const FILENAME = "Feed";

export default {
  async beforeMount() {
    console.log(FILENAME, "beforeMount", "start")

    await this.checkUserState(this);

    this.postList = await this.getFeed(0);

    console.log(FILENAME, this.postList.posts);

    console.log(FILENAME, "beforeMount", "end")
  },

  data() {
    return {
      postList: null,
    }
  },

  methods: {
    ...mapActions(graphStore, { getFeed: 'getFeed' }),
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),
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
        <template v-if="postList.following_count > 0">Your Feed</template>
        <template v-else>Yesterday's top posts</template>
      </h3>
    </div>
    <PostList :postList="postList.posts" :showCreatorStats="true" :showIfHidden="false" />
  </div>
</template>

<style scoped>
</style>
