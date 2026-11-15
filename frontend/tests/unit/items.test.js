import { afterEach, describe, expect, it, vi } from "vitest";

import { createItem, deleteItem, listItems } from "../../src/services/items";

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

describe("serviço de itens", () => {
  it("lista os itens retornados pela API", async () => {
    const items = [
      {
        id: 1,
        name: "Notebook",
        description: "14 polegadas",
      },
    ];

    const fetchMock = vi.fn().mockResolvedValue(mockResponse({ body: items }));

    vi.stubGlobal("fetch", fetchMock);

    await expect(listItems()).resolves.toEqual(items);

    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/items/", {});
  });

  it("informa quando não consegue conectar à API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
    );

    await expect(listItems()).rejects.toThrow(
      "Não foi possível conectar à API.",
    );
  });

  it("utiliza a mensagem detail retornada pela API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        mockResponse({
          ok: false,
          status: 409,
          body: {
            detail: "Já existe um item com esse nome.",
          },
        }),
      ),
    );

    await expect(
      createItem({
        name: "Notebook",
        description: "",
      }),
    ).rejects.toThrow("Já existe um item com esse nome.");
  });

  it("envia o cadastro no formato esperado pelo backend", async () => {
    const created = {
      id: 1,
      name: "Notebook",
      description: "14 polegadas",
    };

    const fetchMock = vi.fn().mockResolvedValue(
      mockResponse({
        status: 201,
        body: created,
      }),
    );

    vi.stubGlobal("fetch", fetchMock);

    await expect(
      createItem({
        name: "Notebook",
        description: "14 polegadas",
      }),
    ).resolves.toEqual(created);

    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/items/", {
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

  it("trata corretamente uma exclusão sem conteúdo", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      mockResponse({
        status: 204,
      }),
    );

    vi.stubGlobal("fetch", fetchMock);

    await expect(deleteItem(5)).resolves.toBeNull();

    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/items/5", {
      method: "DELETE",
    });
  });
});
