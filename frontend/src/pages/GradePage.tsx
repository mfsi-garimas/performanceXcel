import { useState } from "react";
import { gradeSubmission } from "../api/gradingApi";
import "./GradePage.css";
import ResultViewer from "../components/ResultViewer";

const GradePage = () => {
  const [rubricFile, setRubricFile] = useState<File | null>(null);
  const [submissionFile, setSubmissionFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!rubricFile || !submissionFile) {
      setError("Please upload both files");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await gradeSubmission(rubricFile, submissionFile);
      setResult(res);
    } catch (err: any) {
      setError(err?.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>PerformanceXcel</h2>

        <div className="upload-box">
          <label>Upload Rubric</label><br/>
          <input type="file" onChange={(e) => setRubricFile(e.target.files?.[0] || null)} />
          {rubricFile && <p className="success">{rubricFile.name}</p>}
        </div>

        <div className="upload-box">
          <label>Upload Submission</label><br/>
          <input type="file" onChange={(e) => setSubmissionFile(e.target.files?.[0] || null)} />
          {submissionFile && <p className="success">{submissionFile.name}</p>}
        </div>

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Processing..." : "Submit"}
        </button>

        {error && <p className="error">{error}</p>}

        {result && <ResultViewer data={result} />}
      </div>
    </div>
  );
};

export default GradePage;