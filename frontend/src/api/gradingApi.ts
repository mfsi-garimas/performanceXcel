import type { Response } from "../types/response";

const API_URL = import.meta.env.VITE_BACKEND_API_URL + "/api/grade";

export const gradeSubmission = async (
  selectedRubricId?: number,
  submissionFile?: File
): Promise<Response> => {
  const formData = new FormData();

  if (selectedRubricId) formData.append("rubric_id", String(selectedRubricId));
  if (submissionFile) formData.append("submission_file", submissionFile);

  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("User not logged in");
  }

  const response = await fetch(`${API_URL}/`, {
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