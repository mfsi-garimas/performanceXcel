import React from "react";
import styles from "./ResultViewer.module.css";

interface Props {
  data: Record<string, any>;
}

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
    <div className={styles.container}>
      {/* 🔹 Summary */}
      <div className={styles.card}>
        <h2 className={styles.title}>📊 Grading Summary</h2>

        <div className={styles.row}>
          <div>
            <strong>Score:</strong> {TotalScore}
          </div>
          <div>
            <strong>Grade:</strong>{" "}
            <span className={styles.gradeBadge}>{Grade}</span>
          </div>
        </div>

        <p className={styles.text}>
          <strong>Overall:</strong> {OverallGrade}
        </p>

        <div className={styles.progressContainer}>
          <div
            className={styles.progressBar}
            style={{ width: `${percentageValue}%` }}
          />
        </div>

        <p className={styles.text}>{Percentage}</p>
      </div>

      {/* 🔹 Criteria */}
      <div className={styles.card}>
        <h3 className={styles.title}>Criteria Breakdown</h3>

        {Object.entries(criteria).map(([key, value]) => {
          if (typeof value !== "string") return null;

          return (
            <div key={key} className={styles.criteriaRow}>
              <span>{key}</span>
              <span className={styles.tag}>{value}</span>
            </div>
          );
        })}
      </div>

      {/* 🔹 Feedback */}
      {Feedback && (
        <div className={styles.card}>
          <h3 className={styles.title}>Feedback</h3>

          {/* Aligned */}
          {Feedback.AlignedToRubric && (
            <>
              <h4 className={styles.subheading}>Aligned to Rubric</h4>
              {Object.entries(Feedback.AlignedToRubric).map(
                ([key, value]) => (
                  <div key={key}>
                    <h5>{key}</h5>
                    <p className={styles.text}>{value as string}</p>
                  </div>
                )
              )}
            </>
          )}

          {/* Strengths */}
          {Feedback.Strengths && (
            <>
              <h4 className={styles.subheading}>Strengths</h4>
              <ul className={styles.list}>
                {Feedback.Strengths.map((item: string, i: number) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </>
          )}

          {/* Improvements */}
          {Feedback.AreasForImprovement && (
            <>
              <h4 className={styles.subheading}>
                Areas for Improvement
              </h4>
              <ul className={styles.list}>
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
              <h4 className={styles.subheading}>Suggestions</h4>
              <ul className={styles.list}>
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

export default ResultViewer;