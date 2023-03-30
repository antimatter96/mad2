import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../components/Feed.vue')
    },
    {
      path: '/posts/new',
      name: 'newPost',
      component: () => import('../views/NewPost.vue')
    },
    {
      path: '/posts/:post_id',
      name: 'post',
      props: true,
      component: () => import('../components/Post.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/profile/:username',
      name: 'user_profile_page',
      props: true,
      component: () => import('../views/UserProfile.vue')
    },
    {
      path: '/profile/search',
      name: 'user_search_page',
      props: true,
      component: () => import('../views/UserSearch.vue')
    },
    {
      path: '/profile/me/followers',
      name: 'user_followers',
      component: () => import('../views/GraphList.vue')
    },
    {
      path: '/profile/me/following',
      name: 'user_follows',
      component: () => import('../views/GraphList.vue')
    },
    {
      path: '/profile/me/export',
      name: 'export_dashboard',
      component: () => import('../views/ExportDashboard.vue')
    },
  ]
})

export default router
