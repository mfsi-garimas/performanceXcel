import React, { useState } from "react";
import { resetPassword } from "../../api/auth";
import { useSearchParams, useNavigate} from "react-router-dom";
import styles from "./Login.module.css";

const ResetPassword: React.FC = () => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      await resetPassword(token, password);
      setSuccess("Password reset successful 🎉");
      setPassword("");
      setConfirmPassword("");
      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (err: any) {
      setError(err.message || "Reset failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      {/* LEFT */}
      <div className={styles.left}>
        <div className={styles.overlay}>
          <h1 className={styles.title}>Set New Password</h1>
          <p className={styles.tagline}>
            You're one step away from accessing your dashboard 🚀
          </p>
        </div>
      </div>

      {/* RIGHT */}
      <div className={styles.right}>
        <div className={styles.container}>
          <h2 className={styles.heading}>Reset Password</h2>

          <p className={styles.subtitle}>
            Enter your new password below
          </p>

          <form onSubmit={handleSubmit}>
            <div className={styles.inputGroup}>
              <label className={styles.label}>New Password</label>
              <input
                className={styles.input}
                type="password"
                placeholder="Enter new password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className={styles.inputGroup}>
              <label className={styles.label}>Confirm Password</label>
              <input
                className={styles.input}
                type="password"
                placeholder="Confirm new password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>

            {/* Error */}
            {error && <div className={styles.error}>⚠️ {error}</div>}

            {/* Success */}
            {success && <div className={styles.success}>✅ {success}</div>}

            <button
              type="submit"
              disabled={loading}
              className={styles.button}
            >
              {loading ? "Resetting..." : "Reset Password"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;