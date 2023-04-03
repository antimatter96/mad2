<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'
import { postStore } from '../../stores/posts'

import LoadingIcon from '../../components/icons/Loading.vue'

import { getBase64 } from '../../lib/fileUpload'
</script>

<script>
const FILENAME = "EditPost";

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start");

    await this.checkUserState(this);

    console.log(FILENAME, "beforeMount", "this.$route", this.$route);
    this.postId = this.$route.params.post_id;
    console.log(FILENAME, "beforeMount", "this.postId", this.postId);

    let tempPostData = await this.getPost(this.postId);
    console.log(FILENAME, "beforeMount", "tempPostData", tempPostData);

    if (Object.keys(tempPostData).length > 0 && tempPostData.creator.user_id != this.userInfo['user_id']) {
      this.postData = {};
    } else {
      this.postData = tempPostData;
    }

    console.log(FILENAME, "beforeMount", "end");
    this.loading = false;
  },

  data() {
    return {
      loading: true,
      postData: null,
      coverImage: null,
      display_error: null,
      deleteImage: false,
    }
  },

  computed: {
    ...mapState(userAuthStore, ['userInfo']),
  },

  methods: {
    ...mapActions(postStore, { editPost: 'editPost', getPost: 'getPost', deletePost: 'deletePost' }),
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

    async handleDelete(e) {
      e.preventDefault();
      this.loading = true;
      console.log(FILENAME, "handleDelete", "start");

      let deletePost = window.confirm("Do you really want to delete this post ?");
      if (!deletePost) {
        return;
      }

      let result = await this.deletePost(this.postId);
      console.log(FILENAME, "handleDelete", "result", result);

      if (result != null) {
        this.$router.push({
          name: 'user_profile_page',
          params: { username: 'me' }
        });
      } else {
        this.display_error = "Something went wrong. Please try again later";
      }

      console.log(FILENAME, "handleDelete", "end");
      this.loading = false;
    },

    async handleEdit(e) {
      e.preventDefault();
      this.loading = true;
      console.log(FILENAME, "handleEdit", "start");

      this.display_error = null;

      let file = null;
      if (this.coverImage != null) {
        file = await getBase64(this.coverImage);
      }
      console.log(FILENAME, "handleEdit", "file", file);

      let result = await this.editPost(this.postId, {
        title: this.postData.title,
        content: this.postData.content,
        hidden: this.postData.hidden,
        coverImage: file,
        fileName: this.coverImage != null ? this.coverImage.name : null,
        deleteImage: this.deleteImage
      })

      console.log(FILENAME, "handleEdit", "result", result);

      if (result != null) {
        this.$router.push({
          name: 'post',
          params: { post_id: result.post_id }
        });
      } else {
        this.display_error = "Something went wrong. Please try again later";
      }

      console.log(FILENAME, "handleEdit", "start");
      this.loading = false;
    }
  }
}
</script>

<template>
  <div class="px-3">
    <div v-if="postData == null" id="main-loading" class="h-100 w-100">
      <LoadingIcon element="h2" />
    </div>
    <div v-else-if="Object.keys(postData).length > 0" class="col-md-10 offset-md-1 py-2">
      <div>
        <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
      </div>
      <form action="" method="POST" v-on:submit="handleEdit">
        <div class="form-floating mb-2">
          <input type="text" class="form-control fw-bold" id="title" required v-model="postData.title">
          <label for="title" class="fw-bold">Title</label>
        </div>
        <div class="form-floating mb-2">
          <textarea class="form-control fw-light" id="content" required style="height: 20rem;"
            v-model="postData.content"></textarea>
          <label for="title" class="fw-bold">Post</label>
        </div>
        <div class="mb-4 row mx-0 custom-checkbox text-center">
          <div class="col-md-2 d-flex flex-row justify-content-around align-items-center">
            <input type="checkbox" class="form-check-input" id="hidden" v-model="postData.hidden">
            <label for="hidden" class="fw-bold">Hidden</label>
          </div>
          <div class="col-md-10 d-flex flex-row justify-content-around align-items-center">
            <div>
              <input type="checkbox" class="form-check-input" id="deleteImage" v-model="deleteImage">
              <label for="deleteImage" class="fw-bold">Remove cover</label>
            </div>
            <label for="formFile" class="fw-bold">Cover image: <br><span class="fw-light">Leave blank if no
                change</span></label>
            <input type="file" class="form-control form-control-sm fw-light" style="width: 49%; display: inline-block;"
              id="formFile" accept="image/*" v-on:change="coverImageChange">
          </div>
        </div>
        <div class="text-center mb-1">
          <input type="buttion" value="Discard" class="btn btn-warn btn-lg px-5">
          <input type="submit" value="Post" class="btn btn-primary btn-lg px-5">
          <input type="button" value="Delete" class="btn btn-danger btn-lg px-5 mx-4" v-on:click="handleDelete">
        </div>
        <div v-if="display_error != null" class="mt-4 text-danger text-center">
          <span class="fw-bold">Error : {{ display_error }}</span>
        </div>
      </form>
    </div>
    <div v-else class="col-md-10 offset-md-1 text-center text-danger py-5">
      <h2 class="mt-5">Not Found</h2>
    </div>
    <div class="col-md-4 py-2"></div>
  </div>
</template>

<style scoped>
.custom-checkbox {
  border: 0px solid #ced4da;
}
</style>
