<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { apiStore } from '../stores/api'
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
  props: ['user', 'userData', 'showFollowers', 'showFollowing'],
  // 
  computed: {},
  methods: {
    ...mapActions(apiStore, { follow: 'follow', unfollow: 'unfollow' }),

    unfollow() {
      console.log("Here")
    },
    follow() {
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
    <h5 class="mb-0 d-inline-block">
      <RouterLink replace class="text-decoration-none" :to="
        {
          name: 'user_profile_page',
          params: { username: userData.user_id }
        }">{{ userData.email }}
      </RouterLink>

    </h5>
    <template v-if="showFollowing">
      <button v-if="userData.user_follows" v-on:click="unfollow" type="button" class="btn btn-outline-danger px-3 mx-3">
        Unfollow
        <FollowAction :positive="false"></FollowAction>
      </button>
      <button v-else v-on:click="follow" type="button" class="btn btn-outline-success px-3 mx-3">
        Follow
        <FollowAction :positive="true"></FollowAction>
      </button>
    </template>
    <template v-if="showFollowers">
      <button v-if="userData.follows_user" type="button" class="btn btn-outline-info px-3 mx-3">
        Follows You
        <FollowIndicator :positive="true"></FollowIndicator>
      </button>
      <button v-else type="button" class="btn btn-outline-info px-3 mx-3">
        Does not follow You
        <FollowIndicator :positive="false"></FollowIndicator>
      </button>
    </template>
  </div>
</template>

<style scoped>
</style>
