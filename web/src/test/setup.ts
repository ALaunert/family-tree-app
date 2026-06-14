import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/vue";
import { afterEach, vi } from "vitest";

import { resetSessionForTests } from "../app/session";

afterEach(() => {
  resetSessionForTests();
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});
