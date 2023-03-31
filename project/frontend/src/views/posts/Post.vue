<script setup>
import { mapActions, mapState } from 'pinia'
import { RouterLink } from 'vue-router'


import { userAuthStore } from '../../stores/userAuth'
import { postStore } from '../../stores/posts'
import { graphStore } from '../../stores/graph'

import { UPLOADS_BASE_PATH } from '../../config'

import LoadingIcon from '../../components/icons/Loading.vue'
import UserTab from '../../components/UserTab.vue'



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

    this.loading = false;
  },
  async mounted() {
    this.loading = true;
    this.postData = await this.getPost(this.postId);

    console.log("this.postData.hidden", this.postData.hidden == null || this.postData.hidden == false)
    this.loading = false;
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
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    async followersUpdate(operation, user_id) {
      this.loading = true;

      console.log("parent", operation, user_id, "followersUpdate");

      let res = null;
      if (operation == '+') {
        res = await this.follow(user_id);
      } else {
        res = await this.unfollow(user_id);
      }

      if (res == null) {
        this.loading = false;
        return;
      }


      if (operation == '+') {
        this.postData.creator.user_follows = true;
      } else {
        this.postData.creator.user_follows = false;
      }


      this.loading = false;
      console.log(res);
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
          <UserTab :showSummary="true" :userData="postData.creator" :showFollowing="true" :showFollowers="true"
            @followAction="followersUpdate" class="fw-bold d-flex align-items-baseline" style="transform: scale(0.8)" />
        </template>
        <template v-else>
          <h6 class="d-inline-block mb-0 fw-light text-end">Last updated at : {{ postData.updated_at }} <RouterLink
              replace class="text-decoration-none fw-bold" :to="
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
