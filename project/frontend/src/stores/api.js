import { mapActions, mapState } from 'pinia'
import { defineStore } from 'pinia'

import { userAuthStore } from '../stores/userAuth'

const POST_API_BASE = "http://localhost:8080/api/post"
const USER_API_BASE = "http://localhost:8080/api/users"
const FOLLOWERS_API_BASE = "http://localhost:8080/api/followers"


export const apiStore = defineStore('post', {
  state: () => {
    return {
      _loginToken: window.localStorage.getItem("auth_token"),
      _userInfo: null,
      _authStore: userAuthStore()
    }
  },
  getters: {
    loggedIn(state) {
      console.log(state._loginToken, state._loginToken != null, state._userInfo, state._userInfo != null)
      return state._loginToken != null || state._userInfo != null;
    },
    authToken(state) {
      return state._authStore.authToken
    },
  },

  actions: {
    async getPost(id) {
      try {
        let response = await fetch(POST_API_BASE + "/" + id, {
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          }
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(error, "getLoginToken");
        return null;
      }
    },

    async createPost(body) {
      try {
        let response = await fetch(POST_API_BASE, {
          method: 'POST',
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify(body),
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(error, "getLoginToken");
        return null;
      }
    },

    async follow(user_id) {
      try {
        let response = await fetch(FOLLOWERS_API_BASE + '/' + user_id, {
          method: 'POST',
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(error, "getLoginToken");
        return null;
      }
    },

    async unfollow(user_id) {
      try {
        let response = await fetch(FOLLOWERS_API_BASE + '/' + user_id, {
          method: 'DELETE',
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(error, "getLoginToken");
        return null;
      }
    },

    async getUserInfo(user_id) {
      try {
        let response = await fetch(USER_API_BASE + "/" + user_id, {
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          }
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(r)

          return r;
        } else {
          return null;
        }

      } catch (error) {
        console.error(error, "getLoginToken");
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
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          }
        });

        if (response.status == 200) {
          let r = await response.json();

          console.log(r)

          if (followers) {
            return r['followers']
          } else {
            return r['following']
          }

        } else {
          return null;
        }

      } catch (error) {
        console.error(error, "getLoginToken");
        return null;
      }
    },

    setAuthToken(token) {
      this._loginToken = token;
      window.localStorage.setItem("auth_token", token);
    },


  },
})
