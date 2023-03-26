<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { graphStore } from '../stores/graph'
import LoadingIcon from './icons/Loading.vue'
import FollowIndicator from './icons/FollowIndicator.vue'
import FollowAction from './icons/FollowAction.vue'

</script>

<script>
export default {
  // 
  async mounted() {
    console.log(this.userData);
  },
  //
  props: ['user', 'userData', 'showFollowers', 'showFollowing', 'showSummary'],
  // 
  computed: {},
  methods: {
    ...mapActions(graphStore, { follow: 'follow', unfollow: 'unfollow' }),

    unfollow() {
      this.$emit("followersUpdate", "-", this.userData.user_id)
      console.log("Here")
    },
    follow() {
      this.$emit("followersUpdate", "+", this.userData.user_id)
      console.log("Here")
    }
  }
}
</script>

<template>
  <div v-if="userData == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else>
    <h5 v-if="showSummary == true" class="mb-0 d-inline-block">
      <RouterLink replace class="text-decoration-none" :to="
        {
          name: 'user_profile_page',
          params: { username: userData.user_id }
        }">{{ userData.email }}
      </RouterLink>

    </h5>
    <div>
      <template v-if="showFollowing">
        <button v-if="userData.user_follows" v-on:click="unfollow" type="button"
          class="btn btn-outline-danger px-3 mx-3 fw-bold">
          Unfollow
          <FollowAction :positive="false"></FollowAction>
        </button>
        <button v-else v-on:click="follow" type="button" class="btn btn-outline-success px-3 mx-3 fw-bold">
          Follow
          <FollowAction :positive="true"></FollowAction>
        </button>
      </template>
      <!-- <template v-if="showFollowers">
          <button v-if="userData.follows_user" type="button" class="btn btn-outline-info px-3 mx-3 disabled" disabled>
            Follows you
            <FollowIndicator :positive="true"></FollowIndicator>
          </button>
          <button v-else type="button" class="btn px-3 mx-3 disabled" disabled>
            Does not follow you
            <FollowIndicator :positive="false"></FollowIndicator>
          </button>
        </template> -->
      <template v-if="showFollowers">
        <button class="btn disabled fw-light"
          :class="{ 'bg-success': userData.follows_user, 'bg-warning': !userData.follows_user }">
          <template v-if="userData.follows_user">
            <FollowIndicator :positive="true"></FollowIndicator> Follows you
          </template>
          <template v-else>
            <FollowIndicator :positive="false"></FollowIndicator> Does not follow you
          </template>
        </button>
      </template>
    </div>
  </div>
</template>

<style scoped>
</style>
