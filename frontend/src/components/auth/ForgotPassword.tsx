import React, { useState } from "react";
import { forgotPassword } from "../../api/auth";
import styles from "./Login.module.css";

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await forgotPassword(email);
      setSuccess("Password reset link sent to your email");
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      {/* LEFT */}
      <div className={styles.left}>
        <div className={styles.overlay}>
          <h1 className={styles.title}>Reset Your Password</h1>
          <p className={styles.tagline}>
            Secure your account and get back to grading 🚀
          </p>
        </div>
      </div>

      {/* RIGHT */}
      <div className={styles.right}>
        <div className={styles.container}>
          <h2 className={styles.heading}>Forgot Password</h2>

          <p className={styles.subtitle}>
            Enter your email to receive a reset link
          </p>

          <form onSubmit={handleSubmit}>
            <div className={styles.inputGroup}>
              <label className={styles.label}>Email</label>
              <input
                className={styles.input}
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            {/* Error */}
            {error && (
              <div className={styles.error}>
                ⚠️ {error}
              </div>
            )}

            {/* Success */}
            {success && (
              <div className={styles.success}>
                ✅ {success}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className={styles.button}
            >
              {loading ? "Sending..." : "Send Reset Link"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;