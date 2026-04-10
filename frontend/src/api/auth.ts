const API_URL = import.meta.env.VITE_BACKEND_API_URL+"/auth";

export const login = async (email: string, password: string) => {
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    let message = "Login failed";

    if (Array.isArray(data.detail)) {
      message = data.detail[0]?.msg;
    } else if (typeof data.detail === "string") {
      message = data.detail;
    }

    throw new Error(message);
  }

  return data;
};

export const forgotPassword = async (email: string) => {
  const res = await fetch(`${API_URL}/forgot-password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  });

  const data = await res.json();

  if (!res.ok) {
    let message = "Login failed";

    if (typeof data.detail === "string") {
      message = data.detail;
    }

    throw new Error(message);
  }
  return data;
};

export const resetPassword = async (token: string, password: string) => {
  const res = await fetch(`${API_URL}/reset-password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ token, password }),
  });

  if (!res.ok) throw new Error("Reset failed");
  return res.json();
};