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
    console.log("Register.vue", "CREATE START")
    console.log("Login.Register.vue", "CREATE END")
  },
  async created() {
    console.log("Register.vue", "BEFORECREATE START")
    this.loading = true;

    if (!this.loggedIn) {
      await this.checkUserState();
    }

    if (this.loggedIn) {
      console.log("LOGIN PAGE")
      this.loading = false;
      this.$router.push('/');
      this.loading = false;

      return;
    }

    this.loading = false;
    console.log("Register.vue", "CREATE END")

  },
  async beforeMount() {
    console.log("Register.vue", "BEFORE MOUNT START")

    console.log("Register.vue", "BEFORE MOUNT END")
  },
  // INTERNAL STATE
  data() {
    return {
      display_error: null,
      loading: true,
      email: null,
      password: null,
      name: null,
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
      this.loading = true;
      console.log(e);

      this.display_error = null;

      let result = await this.userAuthStoreRegister(this.email, this.password)

      if (result.done) {
        this.$router.push('/login');
      } else {
        if (result.user_error) {
          this.display_error = "Incorrect username / password"
        } else {
          this.display_error = "Something went wrong"
        }
      }

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
        <div><LoadingIcon :element="'h4'" element="h4" :style="{'opacity': (loading? 100: 0)}"></LoadingIcon></div>
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
      <RouterLink to="/login" replace class="fw-bold">Sign In</RouterLink>
    </div>
  </div>

  <div class="col-md-4 py-2"></div>
</template>

<style>
</style>
