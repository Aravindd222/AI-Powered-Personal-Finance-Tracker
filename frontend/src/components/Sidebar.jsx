import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-60 bg-zinc-900 min-h-screen p-4 space-y-4">
      <Link to="/dashboard" className="block text-white hover:text-blue-400">
        Dashboard
      </Link>

      <Link to="/add" className="block text-white hover:text-blue-400">
        Add Expense
      </Link>

      <Link to="/upload" className="block text-white hover:text-blue-400">
        Upload Bill
      </Link>
    </div>
  );
}
