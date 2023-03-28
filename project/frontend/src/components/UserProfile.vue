<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { graphStore } from '../stores/graph'
import LoadingIcon from './icons/Loading.vue'
import UserTab from './UserTab.vue'
import PostSummary from './PostSummary.vue'
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

    this.username = this.$route.params.username;

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

    this.userData = await this.getUserInfo(this.username);
    this.loading = false;

    this.isActuallyUser = this.userData['is_actually_user'];
  },
  async mounted() {
  },
  // 
  data() {
    return {
      msg: "U did it",
      loading: true,
      userData: null,
      username: '',
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
    ...mapActions(graphStore, { getUserInfo: 'getUserInfo', follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    followersUpdate(mode, user_id) {
      console.log("parent", mode, user_id, "followersUpdate");
    }
  }
}
</script>

<template>
  <div v-if="loading" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else-if="userData != null">
    <div class="px-4">
      <div>
        <h3 class="mb-0"> {{ userData.email }} </h3>
        <UserTab v-if="!isActuallyUser" showSummary="false" :userData="userData" :showFollowing="true"
          :showFollowers="true" />
        <h5>
          <template v-if="isActuallyUser">
            <RouterLink to="/profile/me/followers" replace class="fw-bold">
              Followers: {{ userData.followers.length }}
            </RouterLink>
          </template>
          <template v-else>
            Followers: {{ userData.followers.length }}
          </template>
        </h5>
        <h5>
          <template v-if="isActuallyUser">
            <RouterLink to="/profile/me/following" replace class="fw-bold">
              Following: {{ userData.following.length }}
            </RouterLink>
          </template>
          <template v-else>
            Following: {{ userData.following.length }}
          </template>
        </h5>
        <template v-if="isActuallyUser">
          <RouterLink to="/profile/me/export" replace class="fw-bold">
            EXPORT ALL
          </RouterLink>
        </template>
      </div>
    </div>

    <hr>
    <h3>Posts</h3>


    <template v-for="post in userData.posts">
      <PostSummary :postData="post" :showCreatorStats="false" />
      <div> {{ post.post_id }}</div>
      <span v-if="isActuallyUser">
        <span v-if="post.hidden == null">
          NOT HIDDEN
        </span>
        <span v-else>
          {{ post.hidden }}
        </span>

      </span>

    </template>

    <div class="col-md-4 py-4"></div>
    <div class="col-md-4 py-2">
      <div class="card mb-1 px-0">
        <div class="card-header px-2 py-2 mb-0">
          <h5 class="card-title mb-0"> card['title'] </h5>
        </div>
        <div class="card-body px-4">
          <p class="card-text"> card['content'] | replace("\n", "<br>") | safe </p>
          <p class="card-text mb-2"><span class="fw-bold">Due Date: </span> card['deadline'].strftime('%Y-%m-%d') </p>
          <p class="card-text mb-2"><span class="fw-bold">Status: </span>
            {% if card['complete'] %}
            <span class="text-success fw-bold">Completed</span>
            {% else %}
            <span class="text-danger fw-bold">Pending</span>
            {% endif %}
          </p>
          {% if card['complete'] %}
          <p class="card-text mb-2"><span class="fw-bold">Completed On: </span>
            <span class="text-success fw-bold"> card['completed_on'].strftime('%Y-%m-%d') </span>
          </p>
          <p class="card-text mb-2"><span class="fw-bold">Deadline: </span>
            {% if card['deadline_passed'] %}
            <span class="text-danger fw-bold">Missed</span>
            {% else %}
            <span class="text-success fw-bold">Met</span>
            {% endif %}
          </p>
          {% endif %}

        </div>
      </div>
    </div>
    <div class="col-md-4 py-2"></div>
  </div>
  <div v-else>
    <h3>
      Not Found
    </h3>
  </div>
</template>

<style scoped>
</style>
