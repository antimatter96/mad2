const profile = {
  template: `<div>PROFILE</div>`
}

const post = {
  template: `<div>POST</div>`
}


const routes = [
  { path: '/profile', component: profile },
  { path: '/post', component: post },
  { path: '*', component: post },
]

const router = new VueRouter({
  routes,
  base: '/',
})

const app = new Vue({
  router,
  el: "#app",
})
