import { Navigate } from "react-router-dom";
import React from "react";

interface Props {
  children: React.ReactNode;
  roleRequired?: string;
}

const ProtectedRoute = ({ children, roleRequired }: Props) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  if (roleRequired && role !== roleRequired) {
    return <Navigate to="/settings" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;