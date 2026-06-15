import { expect, test, type Page } from "@playwright/test";

async function signIn(page: Page, email = "viewer@example.com") {
  await page.goto("/login");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill("viewer-password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/tree$/);
}

test("renders the empty tree state", async ({ page }) => {
  await page.route("**/api/v1/tree", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      json: {
        viewerRole: "viewer",
        people: [],
        relationships: [],
      },
    });
  });

  await signIn(page);

  await expect(page.getByRole("heading", { name: "Family Tree" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Ada Demo" })).toHaveCount(0);
});

test("opens details after selecting a person", async ({ page }) => {
  await signIn(page);

  await page.getByRole("button", { name: /Ada Demo/ }).click();

  await expect(page.getByRole("complementary", { name: "Person details" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ada Demo" })).toBeVisible();
  await expect(page.getByText("Seeded demo root person")).toBeVisible();
});
