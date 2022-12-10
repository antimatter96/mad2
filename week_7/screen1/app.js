

const privacy = Vue.component('privacy', {
  template:
    `<div>
    <h3>Privacy</h3>
  </div>`
})


const about = Vue.component('about', {
  template:
    `<div>
    <h3>About</h3>
  </div>`
})


const messageBoard = Vue.component('message-board', {
  methods: {
    add_to_total: function () {
      this.$store.commit('incr');
    },
    add_to_total_async: async function () {
      this.$store.dispatch('incr_async');
    }
  },
  computed: {
    grand_total: function () {
      return this.$store.getters.total;
    }
  },
  template: `
  <div>
    <h3>Message board</h3>
    <h5>{{ grand_total }}</h5>
    <button @click="add_to_total">+</button>
    <button @click="add_to_total_async">+</button>
  </div>`
})

const routes = [
  {
    path: '/',
    component: messageBoard
  },
  {
    path: '/about',
    component: about
  },
  {
    path: '/privacy',
    component: privacy
  }
]

const router = new VueRouter({ routes })

var store = new Vuex.Store({
  state: {
    grand_total: 0,
  },
  mutations: {
    incr(state) {
      state.grand_total++;
    }
  },
  getters: {
    total: function (state) {
      return 4 * state.grand_total;
    }
  },
  actions: {
    incr_async: async function (context) {
      await new Promise(function (res, rej) {
        setTimeout(function () {
          res();
        }, 5000)
      })
      context.commit('incr');
    }
  }
});

var app = new Vue({
  el: '#app',
  router,
  store,
})
