import { defineStore } from 'pinia'

import { POST_API_BASE } from '../config'

import { userAuthStore } from './userAuth'

const FILENAME = "stores/posts";

export const postStore = defineStore('post', {
  state: () => {
    return {
      _loginToken: window.localStorage.getItem("auth_token"),
      _authStore: userAuthStore()
    }
  },

  getters: {
    loggedIn(state) {
      console.log(FILENAME, state._loginToken, state._loginToken != null)
      return state._loginToken != null;
    },
    authToken(state) {
      return state._authStore.authToken
    },
  },

  actions: {
    async getPost(id) {
      try {
        let response = await fetch(POST_API_BASE + "/" + id, {
          ...this._commonHeaders(),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "getPost", r)

          return r;
        } else {
          return {};
        }

      } catch (error) {
        console.error(FILENAME, "getPost", error);
        return null;
      }
    },

    async createPost(body) {
      try {
        let response = await fetch(POST_API_BASE, {
          method: 'POST',
          ...this._commonHeaders(),
          body: JSON.stringify(body),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "createPost", r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "createPost", error);
        return null;
      }
    },

    async editPost(post_id, body) {
      try {
        let response = await fetch(POST_API_BASE + '/' + post_id, {
          method: 'PUT',
          ...this._commonHeaders(),
          body: JSON.stringify(body),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "editPost", r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "editPost", error);
        return null;
      }
    },

    async deletePost(post_id) {
      try {
        let response = await fetch(POST_API_BASE + '/' + post_id, {
          method: 'DELETE',
          ...this._commonHeaders(),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "deletePost", r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "deletePost", error);
        return null;
      }
    },

    async exportCSV() {
      try {
        let response = await fetch(POST_API_BASE + "/export/", {
          method: 'POST',
          ...this._commonHeaders(),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "exportCSV", r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "exportCSV", error);
        return null;
      }
    },

    async listExportJobs() {
      try {
        let response = await fetch(POST_API_BASE + "/export/jobs", {
          ...this._commonHeaders(),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "exportCSV", r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "exportCSV", error);
        return null;
      }
    },


    _commonHeaders() {
      return {
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': this.authToken,
        }
      }
    },
  },
})
