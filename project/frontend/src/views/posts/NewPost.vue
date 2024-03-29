<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { postStore } from '../../stores/posts'

import LoadingIcon from '../../components/icons/Loading.vue'

import { getBase64 } from '../../lib/fileUpload'
</script>

<script>
const FILENAME = "NewPost";

export default {
  async beforeMount() {
    console.log(FILENAME, "BEFORE MOUNTED START")
    this.loading = true;

    await this.checkUserState(this);

    console.log(FILENAME, "BEFORE MOUNTED END");
    this.loading = false;
  },

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

  methods: {
    ...mapActions(postStore, { createPost: 'createPost' }),
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),

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
      this.loading = true;
      console.log(FILENAME, "handleSubmit", "start");

      this.display_error = null;

      let file = await getBase64(this.coverImage);

      let result = await this.createPost({
        title: this.title,
        content: this.content,
        hidden: this.hidden,
        coverImage: file,
        fileName: this.coverImage.name,
      })

      console.log(result);

      if (result != null) {
        this.$router.push({
          name: 'post',
          params: { post_id: result.post_id }
        });
      } else {
        this.display_error = "Something went wrong. Please try again later";
      }

      console.log(FILENAME, "handleSubmit", "end");
      this.loading = false;
    }
  }
}
</script>

<template>
  <div class="px-3">
    <div class="col-md-10 offset-md-1 py-2">
      <div>
        <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
      </div>
      <form action="" method="POST" v-on:submit="handleSubmit">
        <div class="form-floating mb-2">
          <input type="text" class="form-control fw-bold" id="title" required v-model="title">
          <label for="title" class="fw-bold">Title</label>
        </div>
        <div class="form-floating mb-2">
          <textarea class="form-control fw-light" id="content" required style="height: 20rem;"
            v-model="content"></textarea>
          <label for="title" class="fw-bold">Post</label>
        </div>
        <div class="mb-4 row mx-0 custom-checkbox text-center">
          <div class="col-md-2 d-flex flex-row justify-content-around align-items-center">
            <input type="checkbox" class="form-check-input" id="hidden" v-model="hidden">
            <label for="hidden" class="fw-bold mx-2">Hidden</label>
          </div>
          <div class="col-md-10 d-flex flex-row justify-content-between align-items-center">
            <label for="formFile" class="fw-light">Cover image:</label>
            <input type="file" class="form-control form-control-sm fw-light" style="width: 74%; display: inline-block;"
              id="formFile" accept="image/*" v-on:change="coverImageChange" required>
          </div>
        </div>
        <div class="text-center mb-4">
          <input type="submit" value="Post" class="btn btn-primary btn-lg px-5">
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
