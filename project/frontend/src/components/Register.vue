<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import LoadingIcon from './icons/Loading.vue'

</script>


<script>

export default {
  // LIFECYCLE
  beforeCreate() {
    console.log("Register.vue", "CREATE START")
    console.log("Login.Register.vue", "CREATE END")
  },
  async created() {
    console.log("Register.vue", "BEFORECREATE START")
    this.loading = true;

    await this.checkUserState()

    console.log("DONE async");

    this.loading = false;

    console.log("Register.vue", "CREATE END")

    if (this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/');
      this.loading = false;

      return;
    }
  },
  async beforeMount() {
    console.log("Register.vue", "BEFORE MOUNT START")

    console.log("Register.vue", "BEFORE MOUNT END")
  },
  // INTERNAL STATE
  data() {
    return {
      msg: "U did it",
      loading: true,
      email: null,
      password: null,
      token: null,
    }
  },

  // COMPUTED
  computed: {
    ...mapState(userAuthStore, ['loggedIn'])

  },


  // METHODS
  methods: {
    ...mapActions(userAuthStore, { userAuthStoreRegister: 'signup', checkUserState: 'checkUserState' }),


    async signup(e) {
      e.preventDefault();
      console.log(e);

      this.userAuthStoreRegister(this.email, this.password)
    }
  }
}
</script>

<template>

  <div class="col-md-4 py-2"></div>
  <div class="col-md-4 py-2">
    <form action="" method="POST" v-on:submit="signup">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
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
        <input type="submit" value="Signup" class="btn btn-primary btn-lg w-100">
      </div>
    </form>

    <div class="mt-2 text-center">
      <RouterLink to="/login" replace class="fw-bold">SIgn In</RouterLink>
    </div>
  </div>
  <div class="col-md-4 py-2"></div>
</template>

<style>

</style>
