import { describe, expect, test, vi } from "vitest";

import { bootstrapSession, setCurrentUser } from "./session";

describe("bootstrapSession", () => {
  test("can force a fresh current-user lookup", async () => {
    setCurrentUser({ id: 1, email: "cached@example.com", role: "viewer" });

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "content-type": "application/json" }),
      json: async () => ({
        user: { id: 2, email: "fresh@example.com", role: "moderator" },
      }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const user = await bootstrapSession({ forceRefresh: true });

    expect(fetchMock).toHaveBeenCalledWith("/api/v1/auth/me", {
      credentials: "include",
      headers: {},
    });
    expect(user).toEqual({
      id: 2,
      email: "fresh@example.com",
      role: "moderator",
    });
  });
});
