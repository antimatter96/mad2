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
  created() {
    console.log("App.vue", "CREATED START")
    console.log("App.vue", "CREATED END")
  },
  async beforeMount() {
    console.log("App.vue", "BEFORE MOUNTED START")
  },
  async mounted() {
    console.log(this.userData);
  },
  //
  props: ['user', 'userData', 'showFollows', 'showFollowing'],
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
  <div v-else class="d-inline-block">
    <div class="px-1">
      <div>
        <h5 class="mb-0"> {{ userData.email }} </h5>
        <div>
          <div>
            <button v-if="userData.user_follows" v-on:click="unfollow" type="button" class="btn btn-outline-danger">
              Unfollow
              <FollowAction v-if="showFollowing" :positive="false"></FollowAction>
            </button>
            <button v-else v-on:click="follow" type="button" class="btn btn-outline-success">
              Follow
              <FollowAction v-if="showFollowing" :positive="true"></FollowAction>
            </button>
          </div>
          <div v-if="showFollowing">
            <button v-if="userData.follows_user" type="button" class="btn btn-outline-info">
              Follows You
              <FollowIndicator :positive="true"></FollowIndicator>
            </button>
            <button v-else type="button" class="btn btn-outline-info">
              Does not follow You
              <FollowIndicator :positive="false"></FollowIndicator>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
