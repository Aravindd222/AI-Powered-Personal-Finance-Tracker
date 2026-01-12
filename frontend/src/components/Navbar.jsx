import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="flex justify-between items-center px-6 py-4 bg-zinc-900 border-b border-zinc-800">
      <h1 className="text-lg font-semibold text-white">
        Finance Tracker
      </h1>

      <button
        onClick={logout}
        className="bg-red-600 px-4 py-1 rounded text-white text-sm"
      >
        Logout
      </button>
    </div>
  );
}
