import React from "react";
import Navbar from "./Navbar";
import styles from "./Layout.module.css";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className={styles.layout}>
      <Navbar />
      <main className={styles.content}>{children}</main>
    </div>
  );
};

export default Layout;