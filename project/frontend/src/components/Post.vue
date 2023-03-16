<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { postStore } from '../stores/api'
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
    ...mapActions(postStore, { getPost: 'getPost' }),
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



    <div class="col-md-4 py-4"></div>
    <div class="col-md-4 py-2 text-center">
      <a class="btn btn-primary btn-sm" href=" url_for('render_edit_card', card_id=card['card_id']) ">Edit</a>
    </div>
    <div class="col-md-4 py-2"></div>
    <div class="col-md-4 py-2"></div>
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
