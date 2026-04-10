import type { GradeResponse } from "../types/grading";

const API_URL = import.meta.env.VITE_BACKEND_API_URL + "/grade";

export const gradeSubmission = async (
  rubricFile?: File,
  submissionFile?: File
): Promise<GradeResponse> => {
  const formData = new FormData();

  if (rubricFile) formData.append("rubric_file", rubricFile);
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