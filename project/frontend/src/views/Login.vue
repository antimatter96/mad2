<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import LoadingIcon from '../components/icons/Loading.vue'

</script>


<script>

export default {
  // LIFECYCLE
  beforeCreate() {
    console.log("Login.vue", "CREATE START")
    console.log("Login.vue", "CREATE END")
  },
  async created() {
    console.log("Login.vue", "BEFORECREATE START")
    this.loading = true;

    await this.checkUserState()

    console.log("DONE async");
    console.log("Login.vue", "CREATE END")

    if (this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/');
      this.loading = false;

      return;
    }

    this.loading = false;
  },
  async beforeMount() {
    console.log("Login.vue", "BEFORE MOUNT START")
    console.log("Login.vue", "BEFORE MOUNT END")
  },
  // INTERNAL STATE
  data() {
    return {
      display_error: null,
      loading: true,
      email: null,
      password: null,
    }
  },

  // COMPUTED
  computed: {
    ...mapState(userAuthStore, ['loggedIn'])
  },

  // METHODS
  methods: {
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    async login(e) {
      e.preventDefault();
      console.log(e);

      this.display_error = null;

      let result = await this.userAuthStoreLogin(this.email, this.password);

      if (result.done) {
        this.$router.push('/');
      } else {
        if (result.user_error) {
          this.display_error = "Incorrect username / password"
        } else {
          this.display_error = "Something went wrong"
        }
      }
    }
  }
}
</script>

<template>
  <div class="offset-md-3 col-md-6 py-2">
    <form action="/" method="POST" v-on:submit="login">
      <div class="form-floating m-2"><br><br></div>
      <div class="form-floating mb-2">
        <input type="email" name="email" class="form-control" required v-model="email">
        <label for="email" class="fw-bold">Email</label>
      </div>
      <div class="form-floating mb-2">
        <input type="password" name="password" class="form-control" required minlength="8" v-model="password">
        <label for="password" class="fw-bold">Password</label>
      </div>
      <div>
        <input type="submit" value="Login" class="btn btn-primary btn-lg w-100">
      </div>

      <div class="mt-2 text-danger" v-if="display_error != null">
        <span class="fw-bold">Error : {{ display_error }}</span>
      </div>

    </form>

    <div class="mt-2 text-center">
      <RouterLink to="/signup" replace class="fw-bold">Sign Up</RouterLink>
    </div>
  </div>

  <div class="col-md-4 py-2"></div>
</template>

<style>
</style>
