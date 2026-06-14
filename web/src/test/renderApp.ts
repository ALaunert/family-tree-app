import { render } from "@testing-library/vue";
import type { Component } from "vue";
import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

export function renderApp(component: Component, routes: RouteRecordRaw[] = []) {
  const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: "/", component }, ...routes],
  });

  return {
    router,
    ...render(component, {
      global: {
        plugins: [router],
      },
    }),
  };
}
