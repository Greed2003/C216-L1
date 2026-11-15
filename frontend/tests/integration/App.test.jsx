import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";

import App from "../../src/App";

function mockResponse({ ok = true, status = 200, body = null } = {}) {
  return {
    ok,
    status,
    json: vi.fn().mockResolvedValue(body),
  };
}

afterEach(() => {
  vi.unstubAllGlobals();
});

it("carrega os itens retornados pela API", async () => {
  const fetchMock = vi.fn().mockResolvedValue(
    mockResponse({
      body: [
        {
          id: 1,
          name: "Notebook",
          description: "14 polegadas",
        },
      ],
    }),
  );

  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  expect(screen.getByText("Carregando itens...")).toBeInTheDocument();

  expect(await screen.findByText("Notebook")).toBeInTheDocument();
  expect(screen.getByText("14 polegadas")).toBeInTheDocument();

  expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/items/", {});
});

it("cadastra um item pela API e o exibe na lista", async () => {
  const user = userEvent.setup();

  const created = {
    id: 1,
    name: "Notebook",
    description: "14 polegadas",
  };

  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce(
      mockResponse({
        body: [],
      }),
    )
    .mockResolvedValueOnce(
      mockResponse({
        status: 201,
        body: created,
      }),
    );

  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  expect(
    await screen.findByText("Nenhum item cadastrado."),
  ).toBeInTheDocument();

  await user.type(screen.getByLabelText("Nome"), "Notebook");
  await user.type(screen.getByLabelText("Descrição"), "14 polegadas");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(await screen.findByText("Notebook")).toBeInTheDocument();
  expect(screen.getByText("14 polegadas")).toBeInTheDocument();

  expect(fetchMock).toHaveBeenNthCalledWith(2, "http://localhost:8000/items/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "Notebook",
      description: "14 polegadas",
    }),
  });
});

it("mostra uma mensagem quando não consegue carregar os itens", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
  );

  render(<App />);

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Não foi possível conectar à API.",
  );
});
