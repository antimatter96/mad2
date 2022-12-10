const player = {
  template: `<div>
    <h1>{{ name }}</h1>
    <router-view />
  </div>`,
  props: ['name']
}
const test = {
  template: `<div>Test</div>`
}

const oneDay = {
  template: `<div>oneDay</div>`
}


const routes = [
  {
    path: '/player/:name',
    component: player,
    children:
      [
        { path: '', component: oneDay },
        { path: 'test', component: test },
        { path: 'oneday', component: oneDay },
      ],
    props: true,
  },

  { path: '*', component: test },
]

const router = new VueRouter({
  routes,
  base: '/',
})

const app = new Vue({
  router,
  el: "#app",
})
