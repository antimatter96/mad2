<script setup>
import { mapActions, mapState } from 'pinia'

import { SSE_BASE_PATH, EXPORT_CSV_BASE_PATH } from '../../config'

import { userAuthStore } from '../../stores/userAuth'
import { graphStore } from '../../stores/graph'
import { postStore } from '../../stores/posts'

import LoadingIcon from '../../components/icons/Loading.vue'
</script>

<script>
const FILENAME = "ExportDashboard"

export default {
  async beforeMount() {
    this.loading = true;
    console.log(FILENAME, "beforeMount", "start")

    await this.checkUserState(this);

    this.jobs = await this.listExportJobs();
    console.log(FILENAME, "jobs", this.jobs);

    console.log(FILENAME, "beforeMount", "end")
    this.loading = false;
  },

  async mounted() {
    this.loading = true;
    console.log(FILENAME, "mounted", "start");

    console.log(FILENAME, "mounted", this.userInfo);

    const channelId = `?channel=users.${this.userInfo['user_id']}`
    const source = new EventSource(SSE_BASE_PATH + channelId, { withCredentials: true });
    source.addEventListener('jobDone', this.sseMessage);
    source.addEventListener('error', this.sseError);
    source.addEventListener('open', this.sseOpen);

    console.log(FILENAME, "mounted", "end");
    this.loading = false;
  },

  data() {
    return {
      loading: true,
      jobs: null,
    }
  },

  computed: {
    ...mapState(userAuthStore, ['userInfo']),
  },

  methods: {
    ...mapActions(graphStore, { getList: 'getList', searchByPrefix: 'searchByPrefix' }),
    ...mapActions(postStore, { exportCSV: 'exportCSV', listExportJobs: 'listExportJobs' }),
    ...mapActions(userAuthStore, { checkUserState: 'checkUserState' }),

    async _export() {
      this.loading = true;
      console.log(FILENAME, "_export", "start");

      let response = await this.exportCSV();
      if (response != null) {
        this.jobs.count++;
        this.jobs.jobs.unshift(response);
      }

      console.log(FILENAME, "_export", "end");
      this.loading = false;
    },

    async sseError(err) {
      console.log(FILENAME, "sseError", err);
      console.error(err);
    },
    async sseOpen(event) {
      console.log(FILENAME, "sseOpen", event);
    },
    async sseMessage(event) {
      this.loading = true;
      console.log(FILENAME, "sseMessage", "start");
      console.log(FILENAME, "sseMessage", event);

      let data = JSON.parse(event.data);
      console.log(FILENAME, "sseMessage", data);
      if (data.message === 'done') {
        this.updateJobStatus(data.job_id);
      }

      console.log(FILENAME, "sseMessage", "end");
      this.loading = false;
    },

    updateJobStatus(job_id) {
      console.log(FILENAME, "updateJobStatus", "start");
      console.log("FILENAME", "updateJobStatus", job_id);

      if (this.jobs == null || this.jobs.jobs == null) {
        return
      }

      for (let i = 0; i < this.jobs.jobs.length; i++) {
        if (this.jobs.jobs[i].job_id == job_id) {
          this.jobs.jobs[i].done = true;
          break;
        }
      }

      console.log(FILENAME, "updateJobStatus", "end");
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
      <div>
        <LoadingIcon :element="'h4'" element="h4" :style="{ 'opacity': (loading ? 100 : 0) }"></LoadingIcon>
      </div>
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
                <span v-else-if="job.done"><a :href="EXPORT_CSV_BASE_PATH + '/' + job.job_id">Download</a></span>
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
