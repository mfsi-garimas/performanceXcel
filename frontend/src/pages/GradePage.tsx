import { useEffect, useState, useRef} from "react";
import {
  gradeSubmission,
  getEvaluations,
  updateEvaluation,
  retryEvaluation
} from "../api/gradingApi";
import styles from "./GradePage.module.css";
import ResultViewer from "./ResultViewer";
import Layout from "../components/Layout";
import { getRubrics } from "../api/rubricApi";

const GradePage = () => {
  const [rubrics, setRubrics] = useState<any[]>([]);
  const [submissionFiles, setSubmissionFiles] = useState<File[]>([]); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedRubricId, setSelectedRubricId] = useState<number | null>(null);
  const [selectedRubricName, setSelectedRubricName] = useState<string | null>(null);
  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [selectedEvaluation, setSelectedEvaluation] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editedName, setEditedName] = useState("");
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [hasPending, setHasPending] = useState(false);


  const fetchDataEvaluations = async () => {
    try {
      const res = await getEvaluations();
      setEvaluations(res.data);

      const pendingExists = res.some(
        (item: any) => item.status !== "completed"
      );

      setHasPending(pendingExists);
    } catch {
      console.error("Failed to load evaluations");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getRubrics();
        setRubrics(res.data);
      } catch {
        console.error("Failed to load rubrics");
      }
    };

    fetchData();
    fetchDataEvaluations();

    if (!hasPending) return;

    const interval = setInterval(fetchDataEvaluations, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async () => {
    if (!selectedRubricId) {
      setError("Please select a rubric");
      return;
    }

    if (submissionFiles.length === 0) {
      setError("Please upload at least one submission");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await gradeSubmission(selectedRubricId, submissionFiles);

      setSubmissionFiles([]);
      setSelectedRubricId(null);
      fetchDataEvaluations();
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (err: any) {
      setError(err?.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (id: number) => {
    try {
      if (!editedName.trim()) return;

      await updateEvaluation(id, editedName);

      setEvaluations((prev) =>
        prev.map((item) =>
          item.id === id
            ? { ...item, student_name: editedName }
            : item
        )
      );

      setEditingId(null);
    } catch (err: any) {
      console.error("Failed to update name", err);
      alert(err.message || "Update failed");
    }
  };

  const handleRetry = async (id: number) => {
    try {
      await retryEvaluation(id);
      fetchDataEvaluations(); 
    } catch (err) {
      console.error("Retry failed", err);
      alert("Retry failed");
    }
  };

  const renderStatusBadge = (status: string) => {
    const config: any = {
      pending: {
        bg: "#f3f4f6",
        color: "#374151",
        label: "Pending",
        icon: "⏳"
      },
      processing: {
        bg: "#fff7ed",
        color: "#c2410c",
        label: "Processing",
        icon: "⚙️",
        animation: "pulse 1.5s infinite"
      },
      extracting: {
        bg: "#eef2ff",
        color: "#4338ca",
        label: "Extracting",
        icon: "📄"
      },
      completed: {
        bg: "#ecfdf5",
        color: "#047857",
        label: "Completed",
        icon: "✅"
      },
      failed: {
        bg: "#fef2f2",
        color: "#b91c1c",
        label: "Failed",
        icon: "❌"
      }
    };

    const current = config[status] || {
      bg: "#f3f4f6",
      color: "#374151",
      label: status
    };

    return (
      <span
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: "6px",
          padding: "6px 10px",
          borderRadius: "999px",
          fontSize: "12px",
          fontWeight: 500,
          background: current.bg,
          color: current.color,
          whiteSpace: "nowrap",
          animation: current.animation
        }}
      >
        <span>{current.icon}</span>
        {current.label}
      </span>
    );
  };

  return (
    <Layout>
      <div className={styles.wrapper}>
        <div className={styles.left}>
          <div className={styles.card}>
            <h2 className={styles.heading}>PerformanceXcel</h2>
            <p className={styles.subtitle}>
              Upload submission(s) to generate evaluation
            </p>

            <div className={styles.uploadBox}>
              <label className={styles.label}>Select Rubric</label>

              <select
                className={styles.input}
                value={selectedRubricId ?? ""}
                onChange={(e) => {
                  const value = e.target.value;
                  const id =value ? Number(value) : null;
                  setSelectedRubricId(id);
                  const selectedRubric = rubrics.find((r) => r.id === id);
                  setSelectedRubricName(selectedRubric ? selectedRubric.rubric_title : null);
                }}
              >
                <option value="">-- Select a rubric --</option>
                {rubrics.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.rubric_title}
                  </option>
                ))}
              </select>

              {selectedRubricName && (
                <p className={styles.fileName}>
                  Selected Rubric: {selectedRubricName}
                </p>
              )}
            </div>

            <div className={styles.uploadBox}>
              <label className={styles.label}>Upload Submissions</label>

              <input
                type="file"
                ref={fileInputRef}
                multiple
                onChange={(e) => {
                  const fileList = e.target.files;
                  if (!fileList) return;

                  const files = Array.from(fileList);
                  setSubmissionFiles(files); 
                }}
              />
            </div>

            {submissionFiles.length > 0 && (
              <div className={styles.fileList}>
                <p><strong>{submissionFiles.length} files selected</strong></p>
                {submissionFiles.map((file, index) => (
                  <p key={index} className={styles.fileName}>
                    {file.name}
                  </p>
                ))}
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={loading || submissionFiles.length === 0}
              className={styles.button}
            >
              {loading ? "Processing..." : "Generate Evaluation"}
            </button>

            {error && <div className={styles.error}>{error}</div>}
          </div>
        </div>

        <div className={styles.right}>
          {evaluations.length === 0 ? (
            <div className={styles.placeholder}>
              <div className={styles.placeholderContent}>
                📊
                <h3>No Evaluations Yet</h3>
                <p>Run evaluation to see results</p>
              </div>
            </div>
          ) : (
            <div className={styles.tableWrapper}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Student Name</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {evaluations.map((item, index) => (
                    <tr key={item.id}>
                      <td>{index + 1}</td>

                      <td>
                        {editingId === item.id ? (
                          <input
                            className={styles.editInput}
                            value={editedName}
                            onChange={(e) => setEditedName(e.target.value)}
                          />
                        ) : (
                          item.student_name || "—"
                        )}
                      </td>

                      <td>{renderStatusBadge(item.status)}</td>

                      <td>
                        {new Date(item.created_date).toLocaleDateString("en-US", {
                          day: "numeric",
                          month: "long",
                          year: "numeric",
                        })}
                      </td>

                      <td className={styles.actionCell}>
                        {editingId === item.id ? (
                          <>
                            <button
                              className={styles.saveBtn}
                              onClick={() => handleSave(item.id)}
                            >
                              Save
                            </button>
                            <button
                              className={styles.cancelBtn}
                              onClick={() => setEditingId(null)}
                            >
                              Cancel
                            </button>
                          </>
                        ) : (
                          <>
                            {item.status === "completed" && (
                              <button
                                className={styles.viewBtn}
                                onClick={() => {
                                  setSelectedEvaluation(item);
                                  setShowModal(true);
                                }}
                              >
                                View
                              </button>
                            )}
                            <button
                              className={styles.editBtn}
                              onClick={() => {
                                setEditingId(item.id);
                                setEditedName(item.student_name || "");
                              }}
                            >
                              Edit
                            </button>

                            {item.status === "failed" && (
                              <button
                                className={styles.retryBtn}
                                onClick={() => handleRetry(item.id)}
                              >
                                Retry
                              </button>
                            )}
                          </>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
            </table>
            </div>
          )}
        </div>
      </div>

      {showModal && selectedEvaluation && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <button
              className={styles.closeBtn}
              onClick={() => setShowModal(false)}
            >
              ✖
            </button>

            <ResultViewer data={selectedEvaluation.evaluation} />
          </div>
        </div>
      )}
    </Layout>
  );
};

export default GradePage;