// stores/main.js
import { defineStore } from 'pinia'

export const mainStore = defineStore('main', {
  state: () => {
    return {
      _loading: true,
    }
  },
  getters: {
    loading() {
      return this._loading
    },
  },

  actions: {
    setLoading() {
      this._loading = true;
    },
    clearLoading() {
      this._loading = false;
    }
  },
})
