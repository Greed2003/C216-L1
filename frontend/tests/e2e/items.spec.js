import { expect, test } from "@playwright/test";

test("cadastra um item e mantém após recarregar a página", async ({ page }) => {
  const uniqueName = `Item E2E ${Date.now()}`;
  const description = "Persistência validada pelo Playwright";

  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Gerenciador de Itens" }),
  ).toBeVisible();

  await page.getByLabel("Nome").fill(uniqueName);
  await page.getByLabel("Descrição").fill(description);

  await page.getByRole("button", { name: "Adicionar" }).click();

  const createdItem = page
    .getByRole("listitem")
    .filter({ hasText: uniqueName });

  await expect(createdItem).toBeVisible();
  await expect(createdItem).toContainText(description);

  await page.reload();

  const persistedItem = page
    .getByRole("listitem")
    .filter({ hasText: uniqueName });

  await expect(persistedItem).toBeVisible();
  await expect(persistedItem).toContainText(description);

  await page.getByLabel("Nome").fill(uniqueName);
  await page.getByLabel("Descrição").fill(description);

  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByRole("alert")).toContainText("Item já existe");

  await expect(page.getByLabel("Nome")).toHaveValue(uniqueName);
  await expect(page.getByLabel("Descrição")).toHaveValue(description);
});
