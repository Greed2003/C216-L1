const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const ITEMS_URL = `${API_URL}/items/`;

function getErrorMessage(payload, fallbackMessage) {
  const detail = payload?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail.map((item) => item?.msg).filter(Boolean);

    if (messages.length > 0) {
      return messages.join(" ");
    }
  }

  return fallbackMessage;
}

async function request(
  url,
  options = {},
  fallbackMessage = "Erro ao realizar a requisição.",
) {
  let response;

  try {
    response = await fetch(url, options);
  } catch {
    throw new Error("Não foi possível conectar à API.");
  }

  if (!response.ok) {
    let payload = null;

    try {
      payload = await response.json();
    } catch {
      payload = null;
    }

    throw new Error(getErrorMessage(payload, fallbackMessage));
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function listItems() {
  return request(ITEMS_URL, {}, "Erro ao carregar os itens.");
}

export function getItem(itemId) {
  return request(`${ITEMS_URL}${itemId}`, {}, "Erro ao carregar o item.");
}

export function createItem({ name, description }) {
  return request(
    ITEMS_URL,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        description: description || null,
      }),
    },
    "Erro ao cadastrar o item.",
  );
}

export function replaceItem(itemId, { name, description }) {
  return request(
    `${ITEMS_URL}${itemId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        description: description || null,
      }),
    },
    "Erro ao substituir o item.",
  );
}

export function updateItem(itemId, values) {
  return request(
    `${ITEMS_URL}${itemId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    },
    "Erro ao atualizar o item.",
  );
}

export function deleteItem(itemId) {
  return request(
    `${ITEMS_URL}${itemId}`,
    {
      method: "DELETE",
    },
    "Erro ao excluir o item.",
  );
}
