import { expect, test, type Page } from "@playwright/test";

async function signInAsModerator(page: Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("moderator@example.com");
  await page.getByLabel("Password").fill("moderator-password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/tree$/);
}

async function addPerson(page: Page, fullName: string) {
  await page.getByRole("button", { name: "Add person" }).click();
  await page.getByLabel("Full name").fill(fullName);
  await page.getByRole("button", { name: "Create person" }).click();
  await expect(page.getByRole("button", { name: fullName })).toBeVisible();
  await page.getByRole("button", { name: "Close editor" }).click();
}

test("moderator adds a person and a relationship", async ({ page }) => {
  const suffix = Date.now();
  const parentName = `E2E Parent ${suffix}`;
  const childName = `E2E Child ${suffix}`;

  await signInAsModerator(page);

  await addPerson(page, parentName);
  await addPerson(page, childName);

  await page.getByRole("button", { name: childName }).click();
  await page.getByRole("button", { name: "Edit person" }).click();
  const relationships = page.getByRole("region", { name: "Relationships" });
  await relationships.getByLabel("Relationship").selectOption("parent");
  await relationships.getByLabel("Person").selectOption({ label: parentName });
  await page.getByRole("button", { name: "Add relationship" }).click();

  await expect(page.getByText(`Parent: ${parentName}`)).toBeVisible();
});
