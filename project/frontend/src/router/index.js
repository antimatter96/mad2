import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/graph/Feed.vue')
    },
    {
      path: '/posts/new',
      name: 'newPost',
      component: () => import('../views/posts/NewPost.vue')
    },
    {
      path: '/posts/:post_id',
      name: 'post',
      props: true,
      component: () => import('../views/posts/Post.vue')
    },
    {
      path: '/posts/edit/:post_id',
      name: 'postEdit',
      props: true,
      component: () => import('../views/posts/EditPost.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/accounts/Login.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/accounts/Register.vue')
    },
    {
      path: '/profile/:username',
      name: 'user_profile_page',
      props: true,
      component: () => import('../views/graph/UserProfile.vue')
    },
    {
      path: '/profile/search',
      name: 'user_search_page',
      props: true,
      component: () => import('../views/graph/UserSearch.vue')
    },
    {
      path: '/profile/me/followers',
      name: 'user_followers',
      component: () => import('../views/graph/GraphList.vue')
    },
    {
      path: '/profile/me/following',
      name: 'user_follows',
      component: () => import('../views/graph/GraphList.vue')
    },
    {
      path: '/profile/me/export',
      name: 'export_dashboard',
      component: () => import('../views/extras/ExportDashboard.vue')
    },
  ]
})

export default router
