import { useEffect, useState } from "react";
import styles from "./Common.module.css";
import { updateUser, getUser } from "../api/userApi";
import Layout from "../components/Layout";

const Settings = () => {

  const [userId, setUserId] = useState<number | null>(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  const fetchUser = async () => {
    try {
      const res = await getUser();

      const user = res.data?.[0];

      if (user) {
        setUsername(user.username ?? "");
        setUserId(user.id ?? "");
      } else {
        setError("No user found");
      }

    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong");
      }
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const handleSave = async () => {
    if (!username.trim()) {
      setError("Username is required");
      return;
    }

    if (!userId) {
      setError("User not found");
      return;
    }

    if (!checkNewPassword()) return;

    setLoading(true);

    try {
      await updateUser(userId, {
        username,
        password
      });

      setStatus("Profile updated successfully");
      setPassword("");
      setConfirmPassword("");
      setError("");
    } catch (err) {
      setError("Update failed");
    } finally {
      setLoading(false);
    }
  };

  const checkNewPassword = () => {
    if (!password) {
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return false;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return false;
    }

    return true;
  };

  return (
  <Layout>
    <div className={styles.authWrapper}>
      <div className={styles.authCard}>
        <h2 className={styles.authTitle}>Account Settings</h2>

        <div className={styles.authField}>
          <label className={styles.authLabel}>Username</label>

          <input
            className={styles.authInput}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className={styles.authField}>
          <label className={styles.authLabel}>New Password</label>

          <input
            className={styles.authInput}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Leave empty to keep current password"
          />
        </div>

        <div className={styles.authField}>
          <label className={styles.authLabel}>Confirm Password</label>

          <input
            className={styles.authInput}
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Leave empty to keep current password"
          />
        </div>

        <button
          className={styles.button}
          onClick={handleSave}
          disabled={loading}
        >
          {loading ? "Saving..." : "Save Changes"}
        </button>

        {status && (
          <div className={styles.authSuccess}>
            {status}
          </div>
        )}

        {error && (
          <div className={styles.authError}>
            {error}
          </div>
        )}
      </div>
    </div>
  </Layout>
);
};

export default Settings;