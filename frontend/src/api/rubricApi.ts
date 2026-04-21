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
  onProgress?: (data: any) => void
) => {
  const formData = new FormData();

  if (rubricFile) formData.append("rubric_file", rubricFile);
  if (rubricTitle) formData.append("rubric_title", rubricTitle);

  const token = localStorage.getItem("token");

  const response = await fetch(`${API_URL}/add-rubric`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.body) throw new Error("No response body");

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let done = false;

  while (!done) {
    const { value, done: doneReading } = await reader.read();
    done = doneReading;

    const chunk = decoder.decode(value, { stream: true });

    const lines = chunk.split("\n").filter(Boolean);

    for (const line of lines) {
      try {
        const parsed = JSON.parse(line);
        onProgress?.(parsed);
      } catch (err) {
        console.error("Invalid JSON chunk", line);
      }
    }
  }
};