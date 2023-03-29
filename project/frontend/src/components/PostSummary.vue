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
export default {
  props: ['postData', 'showCreatorStats', 'followersUpdate'],
  data() {
    return {}
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


    async followAction(mode, user_id) {
      console.log("_followersUpdate", mode, user_id);
      console.log(this.props);
      this.followersUpdate(mode, user_id);
    }
  },
}
</script>

<template>
  <div class="col-md-12 py-2">
    <div class="card mb-1 px-0">
      <div class="card-header px-2 py-2 mb-0">
        <h3 class="card-title mb-0">
          <RouterLink :to="
            {
              name: 'post',
              params: { post_id: postData.post_id }
            }" replace class="text-decoration-none">{{ postData.title }}</RouterLink>

        </h3>
        <h6 class="card-title mb-0"> {{ postData.created_at }} - {{ postData.updated_at }} </h6>
      </div>
      <div v-if="showCreatorStats" class="card-header px-2 py-2 mb-0">
        <UserTab :showSummary="true" :userData="postData.creator" :showFollowing="true" :showFollowers="true"
          class="d-flex align-items-center" @followAction="followAction" />
      </div>
      <div class="card-body px-4">
        {{ postData.content }}
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
