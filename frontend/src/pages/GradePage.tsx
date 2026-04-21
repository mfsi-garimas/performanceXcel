import { useEffect, useState } from "react";
import { gradeSubmission } from "../api/gradingApi";
import styles from "./GradePage.module.css";
import ResultViewer from "../components/ResultViewer";
import Layout from "../components/Layout";
import {getRubrics} from "../api/rubricApi";

const GradePage = () => {
  // const [rubricFile, setRubricFile] = useState<File | null>(null);
  const [rubrics, setRubrics] = useState<any[]>([]);
  const [submissionFile, setSubmissionFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [selectedRubricId, setSelectedRubricId] = useState<number | null>(null);

  useEffect(() => {
      const fetchData = async () => {
        try {
          const res = await getRubrics();
          setRubrics(res.data);
        } catch (err) {
          console.error("Failed to load rubrics");
        }
      };

      fetchData();
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
    setResult(null);

    try {
      const res = await gradeSubmission(selectedRubricId, submissionFile);
      setResult(res);
      setSubmissionFile(null);
      setSelectedRubricId(null);
    } catch (err: any) {
      setError(err?.message || "Something went wrong");
    } finally {
      setLoading(false);
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
        {!result ? (
          <div className={styles.placeholder}>
            <div className={styles.placeholderContent}>
              📊
              <h3>No Evaluation Yet</h3>
              <p>
                Upload files and click "Generate Evaluation" to see results
              </p>
            </div>
          </div>
        ) : (
          <ResultViewer data={result} />
        )}
      </div>
    </div>
  </Layout>
  );
};

export default GradePage;