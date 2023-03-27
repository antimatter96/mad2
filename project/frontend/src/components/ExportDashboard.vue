<script setup>
import { RouterLink } from 'vue-router'
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { graphStore } from '../stores/graph'
import { postStore } from '../stores/posts'
import LoadingIcon from './icons/Loading.vue'

import UserTab from './UserTab.vue'

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
    console.log("App.vue", "BEFORE MOUNTED END")

    this.jobs = await this.listExportJobs();
    console.log(this.jobs)
    this.loading = false;
  },
  async mounted() {
    console.log("App.vue", "MOUNTED START")

    const source = new EventSource("http://localhost:8080/stream", { withCredentials: true });
    source.addEventListener('greeting', async function (event) {
      console.log('event_received', event)
      var data = JSON.parse(event.data);
      console.log("The server says " + data.message);
    });
    source.addEventListener('error', async function (event, xxx) {
      console.log(event, xxx);
      console.error(event);
      console.log(JSON.stringify(event));

      console.log("Failed to connect to event stream. Is Redis running?");
    });
    source.addEventListener('open', async function (event) {
      console.log("open", event);
    });

    console.log("App.vue", "MOUNTED END")
  },
  // 
  data() {
    return {
      loading: true,
      jobs: null,
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
    ...mapActions(graphStore, { getList: 'getList', searchByPrefix: 'searchByPrefix' }),
    ...mapActions(postStore, { exportCSV: 'exportCSV', listExportJobs: 'listExportJobs' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    followersUpdate(a, b) {
      console.log(parent, a, b);
    },

    async search() {
      let response = await this.exportCSV();
      if (response != null) {
        this.jobs.count++;
        this.jobs.jobs.unshift(response);
      }
    },

    jobStatus(job) {
      if (job.done != null && job.done == true) {
        return 'Successfull'
      } else if (job.error != null) {
        return 'Error'
      } else {
        return 'Pending'
      }
    }
  }
}


</script>

<template>
  <div v-if="loading || jobs == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else class="px-3">
    <div class="col-md-10 offset-md-1 border-bottom border-2">
      <h5> Export all your posts <em>[Valid for 1 hour only]</em></h5>
      <div class="text-center mb-3">
        <button class="btn btn-primary fw-bold" type="button" v-on:click="search">Export</button>
      </div>
    </div>
    <div class="mt-4">
      <div v-if="jobs.count > 0" class="col-md-10 offset-md-1">
        <h5>Your Export Jobs</h5>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Export Time</th>
              <th scope="col">Status</th>
              <th scope="col">Download</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, index) in jobs.jobs" :key="job.job_id">
              <td>{{ index + 1 }}</td>
              <td>{{ job.created_at }}</td>
              <td>{{ jobStatus(job) }}</td>
              <td>
                <span v-if="job.expired" class="fw-bold text-danger">Expired</span>
                <span v-else-if="job.deleted">Deleted</span>
                <span v-else-if="job.done"><a
                    :href="'http://localhost:8080/api/post/export/' + job.job_id">Download</a></span>
                <span v-else-if="jobStatus(job) == 'Pending'">❌</span>
                <span v-else-if="jobStatus(job) == 'Error'">❌</span>
                <span v-else>??❌??</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="col-md-10 offset-md-1">
        No export jobs
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
