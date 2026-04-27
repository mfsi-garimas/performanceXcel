import './App.css'
import GradePage from "./pages/GradePage";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/auth/Login";
import ForgotPassword from "./components/auth/ForgotPassword";
import ResetPassword from "./components/auth/ResetPassword";
import ProtectedRoute from "./components/ProtectedRoute";
import RubricPage from "./pages/RubricStorePage";
import UserPage from "./pages/UsersPage";
import SettingsPage from "./pages/SettingsPage";

function App() {
  return <BrowserRouter>
      <Routes>
        <Route
          path="/evaluation"
          element={
            <ProtectedRoute>
              <GradePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/rubric"
          element={
            <ProtectedRoute>
              <RubricPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/users"
          element={
            <ProtectedRoute roleRequired="ADMIN">
              <UserPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <SettingsPage />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
      </Routes>
    </BrowserRouter>
}

export default App
