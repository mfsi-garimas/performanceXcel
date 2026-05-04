import { useEffect, useState } from "react";
import styles from "./RubricStorePage.module.css";
import {
  getUsers,
  createUser,
  updateUser,
  removeUser,
} from "../api/userApi";
import Layout from "../components/Layout";
import type { User } from "../types/types";

const UsersPage = () => {
  const [users, setUsers] = useState<User[]>([]);

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password:"",
    role: "TEACHER",
  });

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editedUser, setEditedUser] = useState<any>({});

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  const fetchUsers = async () => {
    try {
      const res = await getUsers();
      setUsers(res.data);
    } catch {
      setError("Failed to load users");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async () => {
    if (!form.username || !form.email || !form.password) {
      setError("All fields are required");
      return;
    }

    if (form.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    if (form.password !== form.confirm_password) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    setError("");
    setStatus("");

    try {
      await createUser(
        form.username,
        form.email,
        form.password,
        form.role.toUpperCase()
      );

      setStatus("User created successfully");

      await fetchUsers();

      setForm({
        username: "",
        email: "",
        password: "",
        confirm_password:"",
        role: "TEACHER",
      });
    } catch (err: any) {
      setError(err?.message || "Failed to create user");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this user?")) return;

    try {
      await removeUser(id);
      setUsers((prev) => prev.filter((u) => u.id !== id));
    } catch (err: any) {
      setError(err?.message || "Delete failed");
    }
  };

  const handleSave = async (id: number) => {
    try {

      await updateUser(id, {
        username: editedUser.username,
        email: editedUser.email,
        password: editedUser.password,
        role: editedUser.role
      });

      setUsers((prev) =>
        prev.map((u) =>
          u.id === id ? { ...u, ...editedUser } : u
        )
      );

      setEditingId(null);
    } catch {
      setError("Update failed");
    }
  };

  return (
    <Layout>
      <div className={styles.wrapper}>
        <div className={styles.left}>
          <div className={styles.card}>
            <h2 className={styles.title}>User Management</h2>
            <p className={styles.subtitle}>
              Create and manage users
            </p>

            <div className={styles.field}>
              <label className={styles.label}>Username</label>
              <input
                value={form.username}
                onChange={(e) =>
                  setForm({ ...form, username: e.target.value })
                }
                className={styles.input}
                placeholder="Enter username"
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Email</label>
              <input
                value={form.email}
                onChange={(e) =>
                  setForm({ ...form, email: e.target.value })
                }
                className={styles.input}
                placeholder="Enter email"
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Password</label>
              <input
                type="password"
                value={form.password}
                onChange={(e) =>
                  setForm({ ...form, password: e.target.value })
                }
                className={styles.input}
                placeholder="Enter password"
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Confirm Password</label>
              <input
                type="password"
                value={form.confirm_password}
                onChange={(e) =>
                  setForm({ ...form, confirm_password: e.target.value })
                }
                className={styles.input}
                placeholder="Enter password"
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Role</label>
              <select
                value={form.role}
                onChange={(e) =>
                  setForm({ ...form, role: e.target.value })
                }
                className={styles.input}
              >
                <option value="TEACHER">Teacher</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>

            <button
              className={styles.button}
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? "Creating..." : "Create User"}
            </button>

            {error && <div className={styles.error}>{error}</div>}
            {status && <div className={styles.success}>{status}</div>}
          </div>
        </div>

        <div className={styles.right}>
          {users.length === 0 ? (
            <div className={styles.placeholder}>
              <h3>No users yet</h3>
              <p>Create users to see them here</p>
            </div>
          ) : (
            <div className={styles.tableWrapper}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Password</th>
                    <th>Role</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>
                  {users.map((user, index) => (
                    <tr key={user.id}>
                      <td>{index + 1}</td>

                      <td>
                        {editingId === user.id ? (
                          <input
                            className={styles.tableInput}
                            value={editedUser.username}
                            onChange={(e) =>
                              setEditedUser({
                                ...editedUser,
                                username: e.target.value,
                              })
                            }
                          />
                        ) : (
                          user.username
                        )}
                      </td>

                      <td>
                        {editingId === user.id ? (
                          <input
                            className={styles.tableInput}
                            value={editedUser.email}
                            onChange={(e) =>
                              setEditedUser({
                                ...editedUser,
                                email: e.target.value,
                              })
                            }
                          />
                        ) : (
                          user.email
                        )}
                      </td>

                      <td>
                        {editingId === user.id ? (
                          <input
                            className={styles.tableInput}
                            value={editedUser.password}
                            onChange={(e) =>
                              setEditedUser({
                                ...editedUser,
                                password: e.target.value,
                              })
                            }
                          />
                        ) : (
                          "Password"
                        )}
                      </td>

                      <td>
                        {editingId === user.id ? (
                          <select
                            className={styles.tableInput}
                            value={editedUser.role}
                            onChange={(e) =>
                              setEditedUser({
                                ...editedUser,
                                role: e.target.value,
                              })
                            }
                          >
                            <option value="TEACHER">Teacher</option>
                            <option value="ADMIN">Admin</option>
                          </select>
                        ) : (
                          <span
                            className={
                              user.role === "ADMIN"
                                ? styles.adminBadge
                                : styles.teacherBadge
                            }
                          >
                            {user.role}
                          </span>
                        )}
                      </td>

                      <td>
                        {new Date(user.created_date).toLocaleDateString("en-US", {
                          day: "numeric",
                          month: "long",
                          year: "numeric",
                        })}
                      </td>

                      <td className={styles.actions}>
                        {editingId === user.id ? (
                          <>
                            <button
                              className={styles.saveBtn}
                              onClick={() => handleSave(user.id)}
                            >
                              Save
                            </button>

                            <button
                              className={styles.cancelBtn}
                              onClick={() => setEditingId(null)}
                            >
                              Cancel
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              className={styles.editBtn}
                              onClick={() => {
                                setEditingId(user.id);
                                setEditedUser(user);
                              }}
                            >
                              Edit
                            </button>

                            <button
                              className={styles.deleteBtn}
                              onClick={() => handleDelete(user.id)}
                            >
                              🗑
                            </button>
                          </>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default UsersPage;