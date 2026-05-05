import React, { useState } from "react";
import { login } from "../../api/auth";
import styles from "./Login.module.css";
import { jwtDecode } from "jwt-decode";
const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      const decoded: any = jwtDecode(data.access_token);
      localStorage.setItem("role", decoded.role);

      window.location.href = "/rubric";
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      {/* LEFT */}
      <div className={styles.left}>
        <div className={styles.overlay}>
          <h1 className={styles.title}>Performance Xcel</h1>
          <p className={styles.tagline}>
            Evaluate smarter, faster, and better 🚀
          </p>
        </div>
      </div>

      {/* RIGHT */}
      <div className={styles.right}>
        <div className={styles.container}>
          <h2 className={styles.heading}>Welcome Back 👋</h2>
          <p className={styles.subtitle}>
            Welcome back — let’s make grading effortless
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

            <div className={styles.inputGroup}>
              <label className={styles.label}>Password</label>
              <input
                className={styles.input}
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {error && <p className={styles.error}>{error}</p>}

            <div className={styles.forgot}>
              <a href="/forgot-password">Forgot Password?</a>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={styles.button}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;