const API_URL = import.meta.env.VITE_BACKEND_API_URL + "/api";

export const getRubrics = async () => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("User not logged in");
  }

  const res = await fetch(`${API_URL}/get-rubrics`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status === 401 ) {
    localStorage.removeItem("token");
    window.location.href = "/";
    return Promise.reject(new Error("Session expired"));
  }


  return res.json();
};

export const removeRubric = async (rubricId: number) => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("User not logged in");
  }

  const res = await fetch(`${API_URL}/remove-rubric/${rubricId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status === 401 ) {
    localStorage.removeItem("token");
    window.location.href = "/";
    return Promise.reject(new Error("Session expired"));
  }

  if (!res.ok) {
    throw new Error("Failed to delete rubric");
  }

  return res.json();
};

export const uploadRubric = async (
  rubricFile?: File,
  rubricTitle?: string,
): Promise<Response> => {
  const formData = new FormData();

  if (rubricFile) {
    formData.append("rubric_file", rubricFile);
  }

  if (rubricTitle !== undefined) {
    formData.append("rubric_title", rubricTitle);
  }

  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("User not logged in");
  }

  const response = await fetch(`${API_URL}/add-rubric`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  const data = await response.json();

  if (response.status === 401 || data?.detail === "Token is invalid or expired") {
    localStorage.removeItem("token"); 
    window.location.href = "/";
    return Promise.reject(new Error("Session expired"));
  }

  if (!response.ok) {
    let message = "Something went wrong";

    if (Array.isArray(data.detail)) {
      message = data.detail[0]?.msg;
    } else if (typeof data.detail === "string") {
      message = data.detail;
    }

    throw new Error(message);
  }

  return data;
};