import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";

import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AddExpense from "./pages/Addexpense";
import OcrUpload from "./pages/ocrupload";

import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected */}
        <Route
          element={
            <ProtectedRoute>
              <div className="flex min-h-screen bg-zinc-950">
                <Sidebar />
                <div className="flex-1">
                  <Navbar />
                  <div className="p-6">
                    <Outlet />
                  </div>
                </div>
              </div>
            </ProtectedRoute>
         }
      >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/add" element={<AddExpense />} />
          <Route path="/upload" element={<OcrUpload />} />
        </Route>
          
      </Routes>
    </BrowserRouter>
  );
}
