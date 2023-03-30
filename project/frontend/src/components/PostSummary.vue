<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { postStore } from '../stores/posts'
import { graphStore } from '../stores/graph'

import LoadingIcon from './icons/Loading.vue'
import UserTab from './UserTab.vue'
</script>

<script>
const FILENAME = 'PostSummary';
export default {
  props: ['postData', 'showCreatorStats', 'followersUpdate'],
  data() {
    return {}
  },
  beforeMount() {
    console.log(FILENAME, this.postData);
  },
   computed: {
    ...mapState(userAuthStore, ['loggedIn']),
    hideNavBar() {
      return this.loading
    },
  },
  methods: {
    ...mapActions(postStore, { getPost: 'getPost' }),
    ...mapActions(graphStore, { follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),


    splitText() {

      let split = this.postData.content.split('\n');
      let newSplit = [];
      newSplit.push(split[0]);

      let running = ''
      for (let i = 1; i < split.length; i++) {
        running += ' ' + split[i];
        if (running.length > 500) {
          newSplit.push(running);
          running = ''
        }
      }
      newSplit.push(running);
      return newSplit.slice(0, 2);
    },

    async followAction(mode, user_id) {
      console.log("_followersUpdate", mode, user_id);
      console.log(this.props);
      this.followersUpdate(mode, user_id);
    }
  },
}
</script>

<template>
  <div class="card mb-1 px-4">
    <div class="card-header mb-0 text-center bg-white py-3 px-4">
      <h3 class="card-title mb-0">
        <RouterLink :to="
          {
            name: 'post',
            params: { post_id: postData.post_id }
          }" replace class="text-decoration-none">{{ postData.title }}</RouterLink>

      </h3>
    </div>
    <div v-if="showCreatorStats" class="card-header px-0 py-0 mb-0 bg-white align-items-center d-flex">
      <h6 class="d-inline mb-0 fw-light text-end">{{ postData.created_at }}</h6>
      <UserTab :showSummary="true" :userData="postData.creator" :showFollowing="true" :showFollowers="true"
        class="d-inline-flex align-items-center" style="transform: scale(0.7);" @followAction="followAction" />
    </div>
    <div class="card-body px-4">
      <h6>{{ splitText()[0] }}</h6>
      <p>{{ splitText()[1] }}</p>
    </div>
  </div>
</template>

<style scoped>
</style>
