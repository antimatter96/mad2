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

    if (!this.loggedIn) {
      await this.checkUserState()
    }
    if (!this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/login');
      this.loading = false;
    }
    console.log("App.vue", "BEFORE MOUNTED END");

    this.loading = false;
  },
  async mounted() {
  },
  // 
  data() {
    return {
      loading: true,
      title: "",
      content: "",
      hidden: false,
      coverImage: null,
      display_error: null,
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
    ...mapActions(apiStore, { getPost: 'getPost', createPost: 'createPost' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    coverImageChange(fileInput) {
      this.display_error = null;

      let file = fileInput.target.files[0];

      if (file.size > 1024 * 1024 * 100) {
        this.display_error = "size too big"

        fileInput.target.value = null;

        return;
      }

      this.coverImage = file;
    },

    async handleSubmit(e) {
      e.preventDefault();
      console.log(e);

      this.display_error = null;



      function getBase64(file) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => resolve(reader.result.split(',').pop());
          reader.onerror = error => reject(error);
        });
      }

      let file = await getBase64(this.coverImage);

      console.log(file)

      let result = await this.createPost({
        title: this.title,
        content: this.content,
        hidden: this.hidden,
        coverImage: file,
        fileName: this.coverImage.name,
      })

      console.log(result);
      // let result = await this.userAuthStoreLogin(this.email, this.password);

      // if (result.done) {

      // } else {
      //   if (result.user_error) {
      //     this.display_error = "Incorrect username / password"
      //   } else {
      //     this.display_error = "Something went wrong"
      //   }
      // }
    }
  }
}
</script>

<template>
  <div v-if="loading" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else>
    <div class="col-md-4 py-2"></div>
    <div class="col-md-8 col-md-offset-2 py-2">
      <form action="" method="POST" v-on:submit="handleSubmit">
        <div class="form-floating mb-2">
          <input type="text" class="form-control fw-bold" id="title" required v-model="title">
          <label for="title" class="fw-bold">Title</label>
        </div>
        <div class="form-floating mb-2">
          <textarea class="form-control fw-light" id="content" required style="height: 20rem;"
            v-model="content"></textarea>
          <label for="title" class="fw-bold">Summary</label>
        </div>
        <div class="mb-4 row mx-0 custom-checkbox text-center">
          <div class="col-md-3 d-flex flex-row justify-content-around align-items-center">
            <label for="hidden" class="fw-bold mx-2">Hidden</label>
            <input type="checkbox" class="form-check-input" id="hidden" v-model="hidden">
          </div>
          <div class="col-md-9 d-flex flex-row justify-content-between align-items-center">
            <label for="formFile" class="fw-light">Cover image:</label>
            <input type="file" class="form-control form-control-sm fw-light" style="width: 74%; display: inline-block;"
              id="formFile" accept="image/*" v-on:change="coverImageChange" required>
          </div>
        </div>
        <div class="text-center mb-4">
          <input type="submit" value="Post" class="btn btn-primary btn-lg w-25">
        </div>
        <div v-if="display_error != null" class="mt-4 text-danger text-center">
          <span class="fw-bold">Error : {{ display_error }}</span>
        </div>
      </form>
    </div>
    <div class="col-md-4 py-2"></div>
  </div>
</template>

<style scoped>
.custom-checkbox {
  border: 0px solid #ced4da;
}
</style>
