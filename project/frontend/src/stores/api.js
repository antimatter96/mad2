import { mapActions, mapState } from 'pinia'
import { defineStore } from 'pinia'

import { userAuthStore } from '../stores/userAuth'

const API_BASE = "http://localhost:8080/api/post"

export const postStore = defineStore('post', {
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
        let response = await fetch(API_BASE + "/" + id, {
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


    setAuthToken(token) {
      this._loginToken = token;
      window.localStorage.setItem("auth_token", token);
    },

    async checkUserState(login, password) {
      try {
        console.log("checkUserState start")

        await new Promise((resolve, reject) => {
          setTimeout(() => resolve(), 1000)
        });

        console.log("checkUserState main stuff done")
        // this.userData = await api.post({ login, password })
        // showTooltip(`Welcome back ${this.userData.name}!`)

        this._userInfo = true;

        console.log("checkUserState end")
      } catch (error) {
        // showTooltip(error)
        // let the form component display the error
        return error
      }
    },

    async getLoginToken() {
      try {
        let response = await fetch(API_BASE + "/login", {
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json'
          }
        });
        let r = await response.json();

        return r["response"]["csrf_token"];
      } catch (error) {
        console.error(error, "getLoginToken");
        return error
      }
    },

    async getSignupToken() {
      try {

        let response = await fetch(API_BASE + "/register", {
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json'
          }
        });
        let r = await response.json();

        return r["response"]["csrf_token"];
      } catch (error) {
        console.error(error, "getLoginToken");
        return error
      }
    },

    async login(email, password) {
      if (this._csrfToken == null) {
        try {
          this._csrfToken = await this.getLoginToken()
        } catch (e) {
          return { done: false, 'user_error': false };
        }
      }

      try {
        let response = await fetch(API_BASE + "/login?include_auth_token=true", {
          method: 'POST',
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "email": email,
            "password": password,
          })
        });

        if (response.status == 200) {
          let r = await response.json();
          this.setAuthToken(r["response"]["user"]["authentication_token"])
          return { done: true };
        } else if (response.status == 400) {
          return { done: false, 'user_error': true };
        } else {
          return { done: false, 'user_error': false };
        }
      } catch (error) {
        console.log(error);

        return { done: false, 'user_error': false };
      }
    },

    async signup(email, password) {
      if (this._csrfToken == null) {
        try {
          this._csrfToken = await this.getSignupToken();
        } catch (error) {
          return { done: false, 'user_error': false };
        }
      }

      try {
        let response = await fetch(API_BASE + "/register?include_auth_token=true", {
          method: 'POST',
          mode: 'cors', // no-cors, *cors, same-origin
          credentials: 'same-origin', // include, *same-origin, omit
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "email": email,
            "password": password,
          })
        });

        if (response.status == 200) {
          let r = await response.json();
          return { done: true };
        } else if (response.status == 400) {
          return { done: false, 'user_error': true };
        } else {
          return { done: false, 'user_error': false };
        }
      } catch (error) {
        return { done: false, 'user_error': false };
      }
    },
  },
})
