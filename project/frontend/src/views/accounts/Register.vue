<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../../stores/userAuth'

import LoadingIcon from '../../components/icons/Loading.vue'

</script>

<script>
const FILENAME = "Register";

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start")

    if (this.loggedIn) {
      console.log(FILENAME, "Already logged in")
      this.loading = false;
      this.$router.push('/');
      this.loading = false;

      return;
    }

    console.log(FILENAME, "beforeMount", "end")
    this.loading = false;
  },

  data() {
    return {
      display_error: null,
      loading: true,
      email: null,
      password: null,
      name: null,
    }
  },

  computed: {
    ...mapState(userAuthStore, ['loggedIn'])
  },

  methods: {
    ...mapActions(userAuthStore, { userAuthStoreRegister: 'signup', checkUserState: 'checkUserState' }),

    async signup(e) {
      e.preventDefault();
      this.loading = true;
      console.log(FILENAME, "signup", "start")

      this.display_error = null;

      let result = await this.userAuthStoreRegister(this.email, this.password)
      console.log(FILENAME, "signup", "result", result);

      if (result.done) {
        this.$router.push('/login');
      } else {
        if (result.user_error) {
          this.display_error = "Incorrect username / password"
        } else {
          this.display_error = "Something went wrong"
        }
      }

      console.log(FILENAME, "signup", "end")
      this.loading = false;
    }
  }
}
</script>

<template>
  <div class="offset-md-3 col-md-6 py-2">
    <form action="" method="POST" v-on:submit="signup">
      <div>
        <br>
        <div>
          <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
        </div>
      </div>
      <div class="form-floating mb-2">
        <input type="text" name="name" class="form-control" required v-model="name">
        <label for="name" class="fw-bold">Full Name</label>
      </div>
      <div class="form-floating mb-2">
        <input type="email" name="email" class="form-control" required v-model="email">
        <label for="email" class="fw-bold">Email</label>
      </div>
      <div class="form-floating mb-2">
        <input type="password" name="password" class="form-control" required minlength="8" v-model="password">
        <label for="password" class="fw-bold">Password</label>
      </div>
      <div>
        <input type="submit" value="Signup" class="btn btn-primary btn-lg w-100">
      </div>
      <div class="mt-2 text-danger" v-if="display_error != null">
        <span class="fw-bold">Error : {{ display_error }}</span>
      </div>
    </form>
    <div class="mt-2 text-center">
      <RouterLink to="/login" class="fw-bold">Sign In</RouterLink>
    </div>
  </div>
</template>

<style scoped>
</style>
