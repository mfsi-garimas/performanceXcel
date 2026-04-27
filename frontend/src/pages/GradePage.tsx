import { useEffect, useState } from "react";
import { gradeSubmission, getEvaluations, updateEvaluation } from "../api/gradingApi";
import styles from "./GradePage.module.css";
import ResultViewer from "./ResultViewer";
import Layout from "../components/Layout";
import {getRubrics} from "../api/rubricApi";

const GradePage = () => {
  // const [rubricFile, setRubricFile] = useState<File | null>(null);
  const [rubrics, setRubrics] = useState<any[]>([]);
  const [submissionFile, setSubmissionFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedRubricId, setSelectedRubricId] = useState<number | null>(null);
  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [selectedEvaluation, setSelectedEvaluation] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editedName, setEditedName] = useState("");

  useEffect(() => {
      const fetchData = async () => {
        try {
          const res = await getRubrics();
          setRubrics(res.data);
        } catch (err) {
          console.error("Failed to load rubrics");
        }
      };

      const fetchDataEvaluations = async () => {
        try {
          const res = await getEvaluations();
          setEvaluations(res.data);
        } catch (err) {
          console.error("Failed to load rubrics");
        }
      };

      fetchData();
      fetchDataEvaluations();
  }, []);

  const handleSubmit = async () => {
    if (!selectedRubricId) {
      setError("Please select a rubric");
      return;
    }

    if (!submissionFile) {
      setError("Please upload both rubric and submission");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await gradeSubmission(selectedRubricId, submissionFile);
      setSubmissionFile(null);
      setSelectedRubricId(null);
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

  return (
    <Layout>
    <div className={styles.wrapper}>
      {/* LEFT SIDE */}
      <div className={styles.left}>
        <div className={styles.card}>
          <h2 className={styles.heading}>PerformanceXcel</h2>
          <p className={styles.subtitle}>
            Upload rubric and submission to generate evaluation
          </p>

          {/* Rubric */}
          <div className={styles.uploadBox}>
            <label className={styles.label}>Select Rubric</label>

            <select
              className={styles.input}
              value={selectedRubricId ?? ""}
              onChange={(e) => {
              const value = e.target.value;
              setSelectedRubricId(value ? Number(value) : null);
            }}
            >
              <option value="">-- Select a rubric --</option>

              {rubrics.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.rubric_title}
                </option>
              ))}
            </select>

            {selectedRubricId && (
              <p className={styles.fileName}>
                Selected ID: {selectedRubricId}
              </p>
            )}
          </div>

          {/* Submission */}
          <div className={styles.uploadBox}>
            <label className={styles.label}>Upload Submission</label>
            <input
              type="file"
              onChange={(e) =>
                setSubmissionFile(e.target.files?.[0] || null)
              }
            />
            {submissionFile && (
              <p className={styles.fileName}>{submissionFile.name}</p>
            )}
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className={styles.button}
          >
            {loading ? "Processing..." : "Generate Evaluation"}
          </button>

          {error && (
            <div className={styles.error}>{error}</div>
          )}
        </div>
      </div>

      {/* RIGHT SIDE */}
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
          <table className={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Student Name</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {evaluations.map((item, index) => {

                return (
                  <tr key={item.id}>
                    <td>{index + 1}</td>
                    <td>{editingId === item.id ? (
                    <input
                      className={styles.editInput}
                      value={editedName}
                      onChange={(e) => setEditedName(e.target.value)}
                    />
                  ) : (
                    item.student_name || "—"
                  )}</td>
                    <td>
                      {new Date(item.created_date).toLocaleString()}
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
                          <button
                            className={styles.viewBtn}
                            onClick={() => {
                              setSelectedEvaluation(item);
                              setShowModal(true);
                            }}
                          >
                            View
                          </button>

                          <button
                            className={styles.editBtn}
                            onClick={() => {
                              setEditingId(item.id);
                              setEditedName(item.student_name || "");
                            }}
                          >
                            Edit
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
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