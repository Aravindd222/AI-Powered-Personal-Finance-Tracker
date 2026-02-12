import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, register } from "../api/auth";

export default function Login() {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    if (!email || !password) {
      alert("Email and password are required");
      return;
    }

    setLoading(true);

    try {
      if (mode === "login") {
        const data = await login(email, password);
        localStorage.setItem("token", data.access_token);
        navigate("/dashboard");
      } else {
        await register(email, password);
        alert("Account created. Please sign in.");
        setMode("login");
        setPassword("");
      }
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (mode === "login"
          ? "Login failed"
          : "Registration failed");

      alert(msg);
      console.error(err.response?.data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-lg shadow p-8 space-y-6"
      >
        <div>
          <h1 className="text-2xl font-semibold text-white">
            {mode === "login" ? "Sign in" : "Create account"}
          </h1>
          <p className="text-sm text-zinc-400">
            {mode === "login"
              ? "Login to manage your expenses"
              : "Register to start tracking"}
          </p>
        </div>

        <div>
          <label className="block text-sm mb-1 text-zinc-300">Email</label>
          <input
            type="email"
            required
            className="w-full bg-zinc-800 border border-zinc-700 px-3 py-2 rounded text-white"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm mb-1 text-zinc-300">Password</label>
          <input
            type="password"
            required
            className="w-full bg-zinc-800 border border-zinc-700 px-3 py-2 rounded text-white"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-white text-black py-2 rounded disabled:opacity-60"
        >
          {loading
            ? "Please wait..."
            : mode === "login"
            ? "Sign in"
            : "Create account"}
        </button>

        <button
          type="button"
          onClick={() =>
            setMode(mode === "login" ? "register" : "login")
          }
          className="w-full text-sm text-zinc-400 hover:underline"
        >
          {mode === "login"
            ? "New here? Create an account"
            : "Already have an account? Sign in"}
        </button>
      </form>
    </div>
  );
}
