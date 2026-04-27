import { useState, useEffect } from "react";
import styles from "./Navbar.module.css";
import { useNavigate } from "react-router-dom";


const Navbar = () => {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const storedRole = localStorage.getItem("role");
    setRole(storedRole);
  }, []);
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className={styles.navbar}>
      <div className={styles.left}>
        <h2 className={styles.logo}>PerformanceXcel</h2>
      </div>

      <div className={styles.right}>
        <button onClick={() => navigate("/evaluation")} className={styles.link}>Evaluate Submission</button>
        <button onClick={() => navigate("/rubric")} className={styles.link}>Manage Rubrics</button>
        {role === "ADMIN" && (
          <>
            <button onClick={() => navigate("/users")} className={styles.link}>
              Users
            </button>
          </>
        )}
        <button onClick={() => navigate("/settings")} className={styles.link}>Settings</button>
        <button className={styles.logout} onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div
        className={styles.hamburger}
        onClick={() => setOpen(!open)}
      >
        ☰
      </div>

      {open && (
        <div className={styles.mobileMenu}>
          <button onClick={() => navigate("/evaluation")} className={styles.link}>Evaluate Submission</button>
          <button onClick={() => navigate("/rubric")} className={styles.link}>Manage Rubrics</button>
          {role === "ADMIN" && (
            <>
              <button onClick={() => navigate("/users")} className={styles.link}>
                Users
              </button>
            </>
          )}
          <button onClick={() => navigate("/settings")} className={styles.link}>Settings</button>
          <button className={styles.logout} onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </div>
  );
};

export default Navbar;