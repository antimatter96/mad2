<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { postStore } from '../../stores/posts'
import { graphStore } from '../../stores/graph'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserTab from '../../components/UserTab.vue'
import PostSummary from '../../components/PostSummary.vue'
import PostList from '../../components/PostList.vue'

</script>

<script>
const FILENAME = 'Feed';
export default {
  // 
  created() {
    console.log(FILENAME, "CREATED START")
    console.log(FILENAME, "CREATED END")
  },
  async beforeMount() {
    console.log(FILENAME, "BEFORE MOUNTED START")

    console.log("DONE async");

    console.log(this.$route, this.loggedIn);

    if (!this.loggedIn) {
      await this.checkUserState()
    }
    if (!this.loggedIn) {
      console.log("LOGIN PAGE")
      this.$router.push('/login');
      return
    }
    console.log("App.vue", "BEFORE MOUNTED END")

    console.log("mode", this.mode);
    this.postList = await this.getFeed(0);

    console.log(FILENAME, this.postList.posts);
  },
  async mounted() {
  },
  // 
  data() {
    return {
      postList: null,
    }
  },
  // 
  computed: {
    ...mapState(userAuthStore, ['loggedIn']),
  },
  methods: {
    ...mapActions(graphStore, { getFeed: 'getFeed', follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),
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
    <PostList :postList="postList.posts" :showCreatorStats="true" :showIfHidden="false" />
  </div>
</template>

<style scoped>
</style>
