import { useState } from "react";
import styles from "./Navbar.module.css";
import { useNavigate } from "react-router-dom";


const Navbar = () => {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

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

      {/* Mobile Menu */}
      {open && (
        <div className={styles.mobileMenu}>
          <button onClick={() => navigate("/evaluation")} className={styles.link}>Evaluate Submission</button>
          <button onClick={() => navigate("/rubric")} className={styles.link}>Manage Rubrics</button>
          <button className={styles.logout} onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </div>
  );
};

export default Navbar;