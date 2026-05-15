// /src/components/Layout.tsx
import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";

export default function Layout({ children }: { children: ReactNode }) {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  const navItems = [
    { path: "/dashboard", label: "Documents", icon: "📄" },
    { path: "/chat", label: "Chat", icon: "💬" },
    { path: "/notes", label: "Notes", icon: "📒" },
    { path: "/research", label: "Research", icon: "🔬" },
    { path: "/multi-chat", label: "Multi Chat", icon: "🧠" },
    { path: "/flashcards", label: "Flashcards", icon: "⚡" },
    { path: "/quiz", label: "Quiz", icon: "🧪" },
      { path: "/citations", label: "Citations", icon: "📚" },

  ];

  return (
    <div className="app-container">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span className="icon">📘</span>
          <span>ScholarChat</span>
        </div>

        <nav className="nav-links">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${isActive(item.path) ? "active" : ""}`}
            >
              <span className="icon">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <p>ScholarChat v1.0</p>
          <p>© 2024 AI Learning Platform</p>
        </div>
      </aside>

      {/* MAIN AREA */}
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}