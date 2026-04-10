import React from "react";

interface Props {
  data: Record<string, any>;
}

const getColor = (value: string) => {
  if (value === "Unsatisfactory") return "#ef4444"; // red
  if (value === "Partially Proficient") return "#f59e0b"; // yellow
  return "#22c55e"; // green
};

const ResultViewer: React.FC<Props> = ({ data }) => {
  const {
    TotalScore,
    Percentage,
    Grade,
    OverallGrade,
    Feedback,
    ...criteria
  } = data.data;

  const percentageValue = Percentage
    ? parseInt(Percentage.replace("%", ""))
    : 0;

  return (
    <div style={styles.container}>
      {/* 🔹 Summary */}
      <div style={styles.card}>
        <h2>📊 Grading Summary</h2>

        <div style={styles.row}>
          <div>
            <strong>Score:</strong> {TotalScore}
          </div>
          <div>
            <strong>Grade:</strong>{" "}
            <span style={styles.gradeBadge}>{Grade}</span>
          </div>
        </div>

        <p style={{ marginTop: "5px" }}>
          <strong>Overall:</strong> {OverallGrade}
        </p>

        {/* Progress */}
        <div style={styles.progressContainer}>
          <div
            style={{
              ...styles.progressBar,
              width: `${percentageValue}%`,
            }}
          />
        </div>
        <p style={{ fontSize: "12px" }}>{Percentage}</p>
      </div>

      {/* 🔹 Criteria */}
      <div style={styles.card}>
        <h3>Criteria Breakdown</h3>

        {Object.entries(criteria).map(([key, value]) => {
          if (typeof value !== "string") return null; // skip non-strings

          return (
            <div key={key} style={styles.criteriaRow}>
              <span>{key}</span>
              <span style={styles.tag}>{value}</span>
            </div>
          );
        })}
      </div>

      {/* 🔹 Feedback */}
      {Feedback && (
        <div style={styles.card}>
          <h3>Feedback</h3>

          {/* AlignedToRubric */}
          {Feedback.AlignedToRubric && (
            <>
              <h4>Aligned To Rubric</h4>
              {Object.entries(Feedback.AlignedToRubric).map(
                ([key, value]) => (
                  <div key={key} style={{ marginBottom: "10px" }}>
                    <strong>{key}</strong>
                    <p style={styles.text}>{value as string}</p>
                  </div>
                )
              )}
            </>
          )}

          {/* Strengths */}
          {Feedback.Strengths && (
            <>
              <h4>Strengths</h4>
              <ul>
                {Feedback.Strengths.map((item: string, i: number) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </>
          )}

          {/* Areas for Improvement */}
          {Feedback.AreasForImprovement && (
            <>
              <h4>Areas for Improvement</h4>
              <ul>
                {Feedback.AreasForImprovement.map(
                  (item: string, i: number) => (
                    <li key={i}>{item}</li>
                  )
                )}
              </ul>
            </>
          )}

          {/* Suggestions */}
          {Feedback.SuggestionsForRevision && (
            <>
              <h4>Suggestions</h4>
              <ul>
                {Feedback.SuggestionsForRevision.map(
                  (item: string, i: number) => (
                    <li key={i}>{item}</li>
                  )
                )}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    marginTop: "20px",
  },
  card: {
    background: "white",
    padding: "16px",
    borderRadius: "12px",
    marginBottom: "16px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
  },
  gradeBadge: {
    background: "#2563eb",
    color: "white",
    padding: "4px 10px",
    borderRadius: "8px",
  },
  progressContainer: {
    marginTop: "10px",
    background: "#e5e7eb",
    height: "10px",
    borderRadius: "6px",
    overflow: "hidden",
  },
  progressBar: {
    height: "100%",
    background: "#22c55e",
  },
  criteriaRow: {
    display: "flex",
    justifyContent: "space-between",
    padding: "8px 0",
    borderBottom: "1px solid #eee",
  },
  tag: {
    color: "black",
    padding: "4px 8px",
    borderRadius: "6px",
    fontSize: "12px",
  },
  text: {
    fontSize: "14px",
    color: "#555",
  },
};

export default ResultViewer;