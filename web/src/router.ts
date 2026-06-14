import { createRouter, createWebHistory } from "vue-router";

import { bootstrapSession } from "./app/session";
import LoginPage from "./features/auth/LoginPage.vue";

const TreePage = {
  template: `
    <main class="page-shell">
      <section class="panel">
        <h1>Family Tree</h1>
      </section>
    </main>
  `,
};

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/tree" },
    { path: "/login", component: LoginPage },
    { path: "/tree", component: TreePage, meta: { requiresAuth: true } },
  ],
});

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) {
    return true;
  }

  const user = await bootstrapSession();
  if (user === null) {
    return { path: "/login", query: { redirect: to.fullPath } };
  }

  return true;
});
