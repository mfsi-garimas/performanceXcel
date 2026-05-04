import { useState, useEffect } from "react";
import styles from "./Navbar.module.css";
import { useNavigate, useLocation } from "react-router-dom";


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

  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  return (
    <div className={styles.navbar}>
      <div className={styles.left}>
        <img
          src="/performanceXcel-logo.png"
          alt="PerformanceXcel"
          className={styles.logoImage}
        />
      </div>

      <div className={styles.right}>
        <button className={`${styles.link} ${isActive("/rubric") ? styles.active : ""}`} onClick={() => navigate("/rubric")}>Rubrics</button>
        <button onClick={() => navigate("/evaluation")} className={`${styles.link} ${isActive("/evaluation") ? styles.active : ""}`}>Submissions</button>
        {role === "ADMIN" && (
          <>
            <button onClick={() => navigate("/users")} className={`${styles.link} ${isActive("/users") ? styles.active : ""}`}>
              Users
            </button>
          </>
        )}
        <div className={styles.avatarWrapper}>
          <div
            className={styles.avatar}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            👤
          </div>

          {menuOpen && (
            <div className={styles.dropdown}>
              <button className={styles.link}
                onClick={() => {
                  navigate("/settings");
                  setMenuOpen(false);
                }}
              >
                Settings
              </button>

              <button
                onClick={handleLogout}
                className={styles.logoutItem}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>

      <div
        className={styles.hamburger}
        onClick={() => setOpen(!open)}
      >
        ☰
      </div>

      {open && (
        <div className={styles.mobileMenu}>
          <button onClick={() => navigate("/evaluation")} className={styles.link}>Evaluations</button>
          <button onClick={() => navigate("/rubric")} className={styles.link}>Rubrics</button>
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