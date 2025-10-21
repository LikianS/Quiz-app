import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'NewQuizPage',
      component: () => import('../views/NewQuizPage.vue'),
    },
    {
      path: '/questions',
      name: 'QuestionsPage',
      component: () => import('../views/QuestionsManager.vue'),
    },
    {
      path: '/score',
      name: 'ScorePage',
      component: () => import('../views/ScorePage.vue'),
    },
    {
      path: '/questions/:id/edit',
      name: 'AdminQuestionEdit',
      component: () => import('../views/AdminQuestionEdit.vue')
    },
  ],
});

export default router;
