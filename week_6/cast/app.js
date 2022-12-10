

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
  template: `
  <div>
    <h3>Message board</h3>
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


var app = new Vue({
  el: '#app',
  router
})
