// stores/userAuth.js
import { defineStore } from 'pinia'

const API_BASE = "http://localhost:8080/api/accounts"

export const userAuthStore = defineStore('userAuth', {
  state: () => {
    return {
      _loginToken: window.localStorage.getItem("auth_token"),
      _userInfo: null,
      _csrfToken: null,
    }
  },
  getters: {
    loggedIn() {
      console.log(this._loginToken, this._loginToken != null, this._userInfo, this._userInfo != null)
      return this._loginToken != null || this._userInfo != null;
    },
    userInfo() {

    },
  },

  actions: {
    increment() {
      this.count++
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
