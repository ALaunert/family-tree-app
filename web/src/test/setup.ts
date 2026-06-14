import "@testing-library/jest-dom/vitest";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import { cleanup } from "@testing-library/vue";
import { afterEach, vi } from "vitest";

import { resetSessionForTests } from "../app/session";

Object.defineProperties(HTMLElement.prototype, {
  clientHeight: {
    configurable: true,
    value: 620,
  },
  clientWidth: {
    configurable: true,
    value: 960,
  },
});

HTMLElement.prototype.getBoundingClientRect = function getBoundingClientRect() {
  return {
    bottom: 620,
    height: 620,
    left: 0,
    right: 960,
    toJSON: () => ({}),
    top: 0,
    width: 960,
    x: 0,
    y: 0,
  };
};

afterEach(() => {
  resetSessionForTests();
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});
