<script setup>
import { mapActions, mapState } from 'pinia'

import { userAuthStore } from '../stores/userAuth'
import { graphStore } from '../stores/graph'
import { postStore } from '../stores/posts'

import { SSE_BASE_PATH, EXPORT_CSV_BASE_PATH } from '../config'

import LoadingIcon from '../components/icons/Loading.vue'

</script>

<script>
const FILENAME = "ExportDashboard"

export default {
  created() {
    console.log(FILENAME, "CREATED START")
    console.log(FILENAME, "CREATED END")
  },
  async beforeMount() {
    console.log(FILENAME, "BEFORE MOUNTED START")
    this.loading = true;

    if (!this.loggedIn) {
      await this.checkUserState()
    }
    if (!this.loggedIn) {
      console.log(FILENAME, "redirect to LOGIN PAGE")
      this.loading = false;
      this.$router.push('/login');
      this.loading = false;
    }

    this.jobs = await this.listExportJobs();
    console.log(this.jobs)
    this.loading = false;

    console.log(FILENAME, "BEFORE MOUNTED END")
  },
  async mounted() {
    console.log(FILENAME, "MOUNTED START", this.userInfo)

    const channelId = `?channel=users.${this.userInfo['user_id']}`
    const source = new EventSource(SSE_BASE_PATH + channelId, { withCredentials: true });
    source.addEventListener('jobDone', this.sseMessage);
    source.addEventListener('error', this.sseError);
    source.addEventListener('open', this.sseOpen);

    console.log(FILENAME, "MOUNTED END")
  },

  data() {
    return {
      loading: true,
      jobs: null,
    }
  },

  computed: {
    ...mapState(userAuthStore, ['loggedIn', 'userInfo']),
    hideNavBar() {
      return this.loading
    },
  },
  methods: {
    ...mapActions(graphStore, { getList: 'getList', searchByPrefix: 'searchByPrefix' }),
    ...mapActions(postStore, { exportCSV: 'exportCSV', listExportJobs: 'listExportJobs' }),
    ...mapActions(userAuthStore, { userAuthStoreLogin: 'login', checkUserState: 'checkUserState' }),

    async _export() {
      this.loading = true;
      console.log("export", "called")
      let response = await this.exportCSV();
      if (response != null) {
        this.jobs.count++;
        this.jobs.jobs.unshift(response);
      }
      this.loading = false;
    },

    async sseError(event, xxx) {
      console.log(event, xxx);
      console.error(event);
      console.log("Failed to connect to event stream. Is Redis running?");
    },
    async sseOpen(event) {
      console.log("open", event);
    },
    async sseMessage(event) {
      console.log('event_received', event)
      let data = JSON.parse(event.data);
      console.log(data);
      if (data.message === 'done') {
        this.updateJobStatus(data.job_id);
      }
    },

    updateJobStatus(job_id) {
      this.loading = true;

      console.log("updateJobStatus", job_id);
      if (this.jobs != null) {
        if (this.jobs.jobs != null) {
          let target = 0;

          for (let i = 0; i < this.jobs.jobs.length; i++) {
            if (this.jobs.jobs[i].job_id == job_id) {
              this.jobs.jobs[i].done = true;
            }
          }
        }
      }
      this.loading = false;

    },

    jobStatus(job) {
      if (job.done != null && job.done == true) {
        return 'Successful'
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
  <div v-if="jobs == null" id="main-loading" class="h-100 w-100">
    <LoadingIcon element="h2" />
  </div>
  <div v-else class="px-3">
    <div class="col-md-10 offset-md-1 border-bottom border-2">
      <h5> Export all your posts <em>[Valid for 1 hour only]</em></h5>
      <div class="text-center mb-3">
        <button class="btn btn-primary fw-bold" type="button" v-on:click="_export">Export</button>
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
                    :href="EXPORT_CSV_BASE_PATH + '/' + job.job_id">Download</a></span>
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
