import { defineStore } from 'pinia'

import { FOLLOWERS_API_BASE, USER_API_BASE, FEED_API_BASE } from '../config'

import { userAuthStore } from '../stores/userAuth'

const FILENAME = "stores/graph"

export const graphStore = defineStore('graph', {
  state: () => {
    return {
      _loginToken: window.localStorage.getItem("auth_token"),
      _authStore: userAuthStore()
    }
  },

  getters: {
    loggedIn(state) {
      return state._loginToken != null;
    },
    authToken(state) {
      return state._authStore.authToken
    },
  },

  actions: {

    async follow(user_id) {
      try {
        let response = await fetch(FOLLOWERS_API_BASE + '/' + user_id, {
          method: 'POST',
          ...this._commonHeaders()
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "follow", r);

          return {};
        } else if (response.status == 400) {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "follow", error);
        return null;
      }
    },

    async unfollow(user_id) {
      try {
        let response = await fetch(FOLLOWERS_API_BASE + '/' + user_id, {
          method: 'DELETE',
          ...this._commonHeaders()
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "unfollow", r)

          return {};
        } else if (response.status == 400) {
          return null;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "unfollow", error);
        return null;
      }
    },

    async getUserInfo(user_id) {
      try {
        let response = await fetch(USER_API_BASE + "/" + user_id, {
          ...this._commonHeaders()
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "getUserInfo", r)

          if (user_id == 'me') {
            this._authStore.setUserInfo({ user_id: r['user_id'] });
          }

          return r;
        } else if (response.status == 404) {
          return null;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "getUserInfo", error);
        return null;
      }
    },

    async searchByPrefix(prefix) {
      try {
        let response = await fetch(USER_API_BASE + "/" + 'search_by_prefix' + '?prefix=' + encodeURIComponent(prefix), {
          ...this._commonHeaders()
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "searchByPrefix", r)

          return r;
        } else if (response.status == 404) {
          return null;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "searchByPrefix", error);
        return null;
      }
    },

    async getFeed(from) {
      try {
        let response = await fetch(FEED_API_BASE, {
          ...this._commonHeaders()
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(FILENAME, "getFeed", r)

          return r;
        } else if (response.status == 404) {
          return null;
        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "getFeed", error);
        return null;
      }
    },

    async getList(followers) {
      let suffix = "my_follows"
      if (followers) {
        suffix = "follow_me"
      }
      try {
        let response = await fetch(USER_API_BASE + "/" + suffix, {
          ...this._commonHeaders()
        });

        if (response.status == 200) {
          let r = await response.json();

          console.error(FILENAME, "getList", r);

          if (followers) {
            return r['followers']
          } else {
            return r['following']
          }

        } else {
          return null;
        }

      } catch (error) {
        console.error(FILENAME, "getList", error);
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
