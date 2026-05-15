// /src/pages/Register.tsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/client";

export default function Register() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await API.post("/auth/register", {
        username,
        email,
        password,
      });

      alert("Registration successful! You can now log in.");
      navigate("/");
    } catch (error) {
      console.error(error);
      alert("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>📘</div>
          <h1>Create Account</h1>
          <p style={{ color: "var(--text-muted)" }}>Join ScholarChat and start learning with AI</p>
        </div>

        <form onSubmit={handleRegister} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Full Name</label>
            <input
              id="username"
              type="text"
              placeholder="John Doe"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: "1rem" }}>
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account? <Link to="/" style={{ fontWeight: "600" }}>Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}