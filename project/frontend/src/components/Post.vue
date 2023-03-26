<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore, postStore } from '../stores'

import LoadingIcon from './icons/Loading.vue'
import UserTab from './UserTab.vue'



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


    this.mode = "edit"
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
    imageUrl() {
      console.log(this.postData)
      return 'http://localhost:8080/static/user_uploads/' + this.postData.img_url;
    }
  },
  methods: {
    ...mapActions(postStore, { getPost: 'getPost' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),
  }
}
</script>

<template>
  <div v-if="loading" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else-if="postData != null" class="px-4">
    <div class="px-4">
      <h2 class="mb-1"> {{ postData.title }} </h2>
      <div>
        <div v-if="!postData.creator.is_actually_user" class="card-header px-2 py-2 mb-0">
          <UserTab :showSummary="true" :userData="postData.creator" :showFollowing="true" :showFollowers="true" class="bg-red fw-bold d-flex align-items-baseline" />
        </div>
        <div v-else>
          <em>by you</em> Last updated at : {{ postData.updated_at }} EDIT
        </div>
      </div>

      <img :src="imageUrl">

      <h5>
        {{ postData.content }}
      </h5>
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
