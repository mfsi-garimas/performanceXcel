import { useEffect, useState } from "react";
import styles from "./RubricStore.module.css";
import { removeRubric, getRubrics, uploadRubric } from "../api/rubricApi";

interface Rubric {
  id: number;
  rubric_title: string;
  rubric_path: string;
  created_date: string;
}

const RubricStore = () => {
  const API_URL = import.meta.env.VITE_BACKEND_API_URL;

  const [rubrics, setRubrics] = useState<Rubric[]>([]);
  const [rubricFile, setRubricFile] = useState<File | null>(null);
  const [rubricTitle, setRubricTitle] = useState<string>("");

  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<string>("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchRubrics = async () => {
    try {
      const res = await getRubrics();
      setRubrics(res.data);
    } catch (err) {
      console.error("Failed to load rubrics");
    }
  };

  const handleDelete = async (id: number) => {
  try {
    await removeRubric(id);

    setRubrics((prev) => prev.filter((r) => r.id !== id));
  } catch (err: any) {
    setError(err?.message || "Failed to delete rubric");
  }
};

  useEffect(() => {
    fetchRubrics();
  }, []);

  const handleSubmit = async () => {
      if (!rubricFile) {
        setError("Please upload both rubric and submission");
        return;
      }
  
      setLoading(true);
      setError("");
  
      try {
        await uploadRubric(rubricFile, rubricTitle);
        setSuccess("Rubric uploaded");
        await fetchRubrics(); 
        setRubricFile(null);
        setRubricTitle("");
      } catch (err: any) {
        setError(err?.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

  return (
    <div className={styles.wrapper}>
      {/* LEFT */}
      <div className={styles.left}>
        <div className={styles.card}>
          <h2 className={styles.title}>Rubric Library</h2>
          <p className={styles.subtitle}>
            Upload and manage your rubrics
          </p>

          <div className={styles.field}>
            <label className={styles.label}>Rubric Title</label>
            <input
              type="text"
              value={rubricTitle}
              onChange={(e) => setRubricTitle(e.target.value)}
              className={styles.input}
              placeholder="Enter rubric title"
            />
          </div>

          <div className={styles.uploadBox}>
            <label className={styles.label}>Upload Rubric</label>
            <input
              type="file"
              onChange={(e) =>
                setRubricFile(e.target.files?.[0] || null)
              }
            />
          
          </div>

          <button
            className={styles.button}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Uploading..." : "Upload File"}
          </button>
          {error && (
            <div className={styles.error}>⚠️ {error}</div>
          )}
          {success && (
            <div className={styles.success}>{success}</div>
          )}
        </div>
      </div>

      {/* RIGHT */}
      <div className={styles.right}>
        {rubrics.length === 0 ? (
          <div className={styles.placeholder}>
            <h3>No rubrics yet</h3>
            <p>Upload rubrics to see them here</p>
          </div>
        ) : (
          <div className={styles.grid}>
            {rubrics.map((item) => {
              let images: string[] = [];

              try {
                images = JSON.parse(item.rubric_path || "[]");
              } catch {
                images = [];
              }

              return (
                <div key={item.id} className={styles.cardItem}>
                  
                  {/* TITLE */}
                  <h3 className={styles.title}>
                    {item.rubric_title || "Untitled"}
                  </h3>

                  {/* IMAGES */}
                  <div className={styles.imageGrid}>
                    {images.map((img, index) => (
                      <img
                        key={index}
                        src={`${API_URL}/${img}`}
                        className={styles.image}
                        alt={`rubric-${item.id}-${index}`}
                        onClick={() => setSelectedImage(`${API_URL}/${img}`)}
                      />
                    ))}
                  </div>

                  <button
                    className={styles.deleteBtn}
                    onClick={() => handleDelete(item.id)}
                  >
                    🗑
                  </button>

                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* MODAL */}
      {selectedImage && (
        <div
          className={styles.modal}
          onClick={() => setSelectedImage("")}
        >
          <img src={selectedImage} className={styles.modalImage} />
        </div>
      )}
    </div>
  );
};

export default RubricStore;