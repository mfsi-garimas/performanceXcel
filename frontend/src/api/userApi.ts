const API_URL = import.meta.env.VITE_BACKEND_API_URL + "/api/user";

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("User not logged in");
  }

  return {
    Authorization: `Bearer ${token}`,
  };
};

export const getUsers = async () => {

  const res = await fetch(`${API_URL}/get-users`, {
    method: "GET",
    headers: getAuthHeaders()
  });

  if (res.status === 401 ) {
    localStorage.removeItem("token");
    window.location.href = "/";
    return Promise.reject(new Error("Session expired"));
  }

  if (!res.ok) throw new Error("Failed to fetch users");

  return res.json();
};

export const getUser = async () => {

  const res = await fetch(`${API_URL}/get-user`, {
    method: "GET",
    headers: getAuthHeaders()
  });

  if (res.status === 401 ) {
    localStorage.removeItem("token");
    window.location.href = "/";
    return Promise.reject(new Error("Session expired"));
  }

  if (!res.ok) throw new Error("Failed to fetch users");

  return res.json();
};

export const removeUser = async (userId: number) => {
  const res = await fetch(`${API_URL}/remove-user/${userId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/";
    throw new Error("Session expired");
  }

  if (!res.ok) throw new Error("Failed to delete user");

  return res.json();
};

export const updateUser = async (
  userId: number,
  username?: string,
  email?: string,
  password?: string,
  role?: string
) => {
  const res = await fetch(`${API_URL}/update-user/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({
      username,
      email,
      password,
      role,
    }),
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/";
    throw new Error("Session expired");
  }

  if (!res.ok) throw new Error("Failed to update user");

  return res.json();
};

export const createUser = async (
  username: string,
  email: string,
  password: string,
  role: string
) => {
  const res = await fetch(`${API_URL}/create-user`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({
      username,
      email,
      password,
      role,
    }),
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/";
    throw new Error("Session expired");
  }

  if (!res.ok) throw new Error("Failed to create user");

  return res.json();
};