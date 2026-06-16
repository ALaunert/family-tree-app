import { expect, test } from "@playwright/test";

test("redirects unauthenticated tree visitors to login", async ({ page }) => {
  await page.goto("/tree");

  await expect(page).toHaveURL(/\/login\?redirect=\/tree$/);
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
});
