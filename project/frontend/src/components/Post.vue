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
    this.loading = true;

    console.log("DONE async");

    console.log(this.$route);

    this.postId = this.$route.params.post_id;

    if (!this.loggedIn) {
      await this.checkUserState()
    }
    if (!this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/login');
      this.loading = false;
    }
    console.log("App.vue", "BEFORE MOUNTED END")

    this.postData = await this.getPost(this.postId);
    this.loading = false;
  },
  async mounted() {
  },
  // 
  data() {
    return {
      msg: "U did it",
      loading: true,
      postData: null,
      postId: '',
    }
  },
  // 
  computed: {
    ...mapState(userAuthStore, ['loggedIn']),
    hideNavBar() {
      return this.loading
    },
  },
  methods: {
    ...mapActions(apiStore, { getPost: 'getPost' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),
  }
}
</script>

<template>
  <div v-if="loading" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else-if="postData != null">
    <div class="col-md-4 py-4"></div>
    <div class="px-1">
      <div>
        <h3 class="mb-0"> {{ postData.title }} </h3>
        <div>
          <h5>by {{ postData.creator_id }}</h5>
          <h6>
            {{ postData.created_at }}
          </h6>
          <h6>
            {{ postData.updated_at }}
          </h6>
        </div>

        <h5>
          {{ postData.content }}
        </h5>
      </div>
    </div>
  </div>
  <div v-else>
    <h3>
      Not Found
    </h3>
  </div>
</template>

<style scoped>
</style>
