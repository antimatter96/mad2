<script setup>
import { mapActions, mapState } from 'pinia'
import { RouterLink } from 'vue-router'


import { userAuthStore } from '../../stores/userAuth'
import { postStore } from '../../stores/posts'
import { graphStore } from '../../stores/graph'

import { UPLOADS_BASE_PATH } from '../../config'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserSummary from '../../components/UserSummary.vue'



</script>

<script>
const FILENAME = "Post";

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start")

    await this.checkUserState(this);

    this.postId = this.$route.params.post_id;

    this.postData = await this.getPost(this.postId);

    console.log("this.postData.hidden", this.postData.hidden == null || this.postData.hidden == false)

    console.log(FILENAME, "mounted", "end")
    this.loading = false;
  },

  data() {
    return {
      loading: true,
      postData: null,
      postId: '',
    }
  },

  computed: {
    splitText() {
      let split = this.postData.content.split('\n');
      let newSplit = [];
      newSplit.push(split[0] + ' ' + split[1]);

      let running = ''
      for (let i = 2; i < split.length; i++) {
        running += ' ' + split[i];
        if (running.length > 500) {
          newSplit.push(running);
          running = ''
        }
      }
      newSplit.push(running);
      return newSplit;
    },

    imageUrl() {
      console.log(this.postData.img_url)
      if (this.postData.img_url != null) {
        return UPLOADS_BASE_PATH + '/' + this.postData.img_url;
      }

      return ''
    }
  },

  methods: {
    ...mapActions(postStore, { getPost: 'getPost' }),
    ...mapActions(graphStore, { follow: 'follow', unfollow: 'unfollow' }),
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),

    async followersUpdate(operation, user_id) {
      this.loading = true;
      console.log(FILENAME, "followersUpdate", "start");
      console.log(FILENAME, "followersUpdate", { operation, user_id });

      let action = operation == '+' ? this.follow : this.unfollow;

      let res = await action(user_id);
      if (res == null) {
        this.loading = false;
        return;
      }

      if (operation == '+') {
        this.postData.creator.user_follows = true;
      } else {
        this.postData.creator.user_follows = false;
      }

      console.log(FILENAME, "followersUpdate", "start");
      this.loading = false;
    },
  }
}
</script>

<template>
  <div v-if="postData == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else-if="Object.keys(postData).length > 0" class="col-md-12 px-6"
    :style="{ backgroundImage: `linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),url(${imageUrl})` }">
    <div>
      <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"
        style="transform: scale(0.7);"></LoadingIcon>
    </div>
    <div class="boder-2 border-bottom mb-4">
      <h2 class="mb-1 text-center"> {{ postData.title }} </h2>
      <div class="align-items-center d-flex card-header px-0 py-0 mb-0 justify-content-between">
        <template v-if="!postData.creator.is_actually_user">
          <h6 class="d-inline-block mb-0 fw-light text-end">Created : {{ postData.created_at }}</h6>
          <UserSummary :showSummary="true" :userData="postData.creator" :showFollowing="true" :showFollowers="true"
            @followAction="followersUpdate" class="fw-bold d-flex align-items-baseline" style="transform: scale(0.8)" />
        </template>
        <template v-else>
          <h6 class="d-inline-block mb-0 fw-light text-end">Last updated at : {{ postData.updated_at }} <RouterLink
              class="text-decoration-none fw-bold" :to="
                {
                  name: 'postEdit',
                  params: { post_id: postId }
                }"><em>Edit</em>
            </RouterLink>
          </h6>
          <h6 class="d-inline-block mb-0 fw-bold text-success" v-if="postData.hidden == null || postData.hidden == false">
            Visible
          </h6>
          <h6 class="d-inline-block mb-0 fw-bold text-danger" v-else>
            Hidden
          </h6>
          <h6 class="d-inline-block mb-0 fw-bold text-end">by you</h6>
        </template>
      </div>
    </div>
    <div>
      <h6 class="subhead">{{ splitText[0] }}</h6>
      <p v-for="para in splitText.slice(1)">
        {{ para }}
      </p>
    </div>
  </div>
  <div v-else class="col-md-10 offset-md-1 text-center text-danger py-5">
    <h2 class="mt-5">Not Found</h2>
  </div>
</template>

<style scoped>
.subhead {
  font-family: serif;
  font-size: 1.25rem;
}

.subhead::first-letter {
  initial-letter: 2 1;
  font-weight: bold;
  margin-right: .5em;
}
</style>
