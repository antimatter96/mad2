import { defineStore } from 'pinia'

import { ACCOUNTS_API_BASE } from '../config'

const FILENAME = 'userAuth.js'

export const userAuthStore = defineStore('userAuth', {
  state: () => {
    return {
      _loginToken: window.localStorage.getItem("auth_token"),
      _userInfo: window.localStorage.getItem("user_info") != null ? JSON.parse(window.localStorage.getItem("user_info")) : null,
      _csrfToken: null,
    }
  },
  getters: {
    loggedIn(state) {
      console.log(FILENAME, "loggedIn", state._loginToken, state._loginToken != null);
      return state._loginToken != null;
    },
    userInfo(state) {
      return state._userInfo;
    },
    authToken(state) {
      return state._loginToken;
    }
  },

  actions: {
    setAuthToken(token) {
      this._loginToken = token;
      window.localStorage.setItem("auth_token", token);
    },

    setUserInfo(info) {
      this._userInfo = info;
      window.localStorage.setItem("user_info", JSON.stringify(this._userInfo));
    },

    logout() {
      window.localStorage.setItem("user_info", null);
      window.localStorage.setItem("auth_token", null);
      this._loginToken = null;
      this._userInfo = null;
    },

    async checkUserState(login, password) {
      try {
        console.log(FILENAME, "checkUserState start")

        await new Promise((resolve, reject) => {
          setTimeout(() => resolve(), 1000)
        });

        console.log(FILENAME, "checkUserState main stuff done")
        // this.userData = await api.post({ login, password })
        // showTooltip(`Welcome back ${this.userData.name}!`)

        console.log(FILENAME, "checkUserState end")
      } catch (error) {
        // showTooltip(error)
        // let the form component display the error
        return error
      }
    },

    async getLoginToken() {
      try {

        let response = await fetch(ACCOUNTS_API_BASE + "/login", {
          ...this._commonHeaders(),
        });
        let r = await response.json();

        return r["response"]["csrf_token"];
      } catch (error) {
        console.error(FILENAME, error, "getLoginToken");
        return error
      }
    },

    async getSignupToken() {
      try {

        let response = await fetch(ACCOUNTS_API_BASE + "/register", {
          ...this._commonHeaders(),
        });
        let r = await response.json();

        return r["response"]["csrf_token"];
      } catch (error) {
        console.error(FILENAME, error, "getLoginToken");
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
        let response = await fetch(ACCOUNTS_API_BASE + "/login?include_auth_token=true", {
          method: 'POST',
          ...this._commonHeaders(),
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
        console.log(FILENAME, error);
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
        let response = await fetch(ACCOUNTS_API_BASE + "/register?include_auth_token=true", {
          method: 'POST',
          ...this._commonHeaders(),
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

    _commonHeaders() {
      return {
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
        }
      }
    },
  },
})
