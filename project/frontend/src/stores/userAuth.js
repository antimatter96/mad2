import { defineStore } from 'pinia'

import { ACCOUNTS_API_BASE } from '../config'

const FILENAME = "stores/userAuth";


const AUTH_TOKEN = "auth_token";
const USER_INFO = "user_info";

export const userAuthStore = defineStore('userAuth', {
  state: () => {
    return {
      _loginToken: window.localStorage.getItem(AUTH_TOKEN),
      _userInfo: window.localStorage.getItem(USER_INFO) != null ? JSON.parse(window.localStorage.getItem(USER_INFO)) : null,
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
      window.localStorage.setItem(AUTH_TOKEN, token);
    },

    setUserInfo(info) {
      this._userInfo = info;
      window.localStorage.setItem(USER_INFO, JSON.stringify(this._userInfo));
    },

    logout() {
      window.localStorage.removeItem(USER_INFO);
      window.localStorage.removeItem(AUTH_TOKEN);
      this._loginToken = null;
      this._userInfo = null;
    },

    async checkUserState(component) {
      console.log(FILENAME, "checkUserState", "start")

      if (component == null || component == undefined) {
        return;
      }

      if (!this.loggedIn) {
        if (component.$router && component.$router.push) {
          component.$router.push('/login');
        }
      }

      console.log(FILENAME, "checkUserState", "end")
    },

    async getLoginToken() {
      console.log(FILENAME, "getLoginToken", "start")

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
      console.log(FILENAME, "getSignupToken", "start")

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
      console.log(FILENAME, "login", "start")

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

    async signup(email, password, name) {
      console.log(FILENAME, "signup", "start")

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
            "name": name,
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
