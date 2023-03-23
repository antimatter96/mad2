<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { apiStore } from '../stores/api'
import LoadingIcon from './icons/Loading.vue'


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
  props: ['user', 'userData'],
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
    <div class="px-1">
      <div>
        <h5 class="mb-0"> {{ userData.email }} <span> |||||  </span>
          <span v-if="userData.user_follows" v-on:click="unfollow">Unfollow</span>
          <span v-else v-on:click="follow">FOLLOW</span>
          <span>||</span>
          <span v-if="userData.follows_user">Follows You</span>
          <span v-else>Doesn't Follow You</span>
        </h5>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
