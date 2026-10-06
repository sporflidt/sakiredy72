const API = ""; // mismo origen: el Gateway sirve el frontend

async function apiRequest(path, options = {}) {
    return fetch(`${API}${path}`, {
        ...options,
        credentials: "include",
        headers: {
            ...(options.headers || {}),
            "Content-Type": "application/json"
        }
    });
}
