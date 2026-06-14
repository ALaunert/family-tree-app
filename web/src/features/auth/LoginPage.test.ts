import { render, screen } from "@testing-library/vue";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";

import LoginPage from "./LoginPage.vue";

describe("LoginPage", () => {
  test("submits credentials and redirects to /tree on success", async () => {
    const push = vi.fn();
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "content-type": "application/json" }),
      json: async () => ({
        user: { id: 1, email: "owner@example.com", role: "owner" },
      }),
    });

    vi.stubGlobal("fetch", fetchMock);

    render(LoginPage, {
      global: {
        mocks: {
          $router: { push },
        },
      },
    });

    await userEvent.type(screen.getByLabelText("Email"), "owner@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "change-me");
    await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

    expect(fetchMock).toHaveBeenCalledWith("/api/v1/auth/login", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "owner@example.com",
        password: "change-me",
      }),
    });
    expect(push).toHaveBeenCalledWith("/tree");
  });
});
