import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

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
      component: () => import('../components/NewPost.vue')
    },
    {
      path: '/posts/:post_id',
      name: 'post',
      props: true,
      component: () => import('../components/Post.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
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
      component: () => import('../components/UserProfile.vue')
    },
    {
      path: '/profile/me/followers',
      name: 'user_followers',
      component: () => import('../components/GraphList.vue')
    },
    {
      path: '/profile/me/following',
      name: 'user_follows',
      component: () => import('../components/GraphList.vue')
    },
  ]
})

export default router
