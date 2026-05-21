// /src/routes/AppRouter.tsx

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";

import ProtectedRoute from "../components/ProtectedRoute";

import Dashboard from "../pages/Dashboard";
import Chat from "../pages/Chat";
import Notes from "../pages/Notes";
import Flashcards from "../pages/Flashcards";
import Quiz from "../pages/Quiz";
import Research from "../pages/Research";
import MultiChat from "../pages/MultiChat";
import DocumentDetail from "../pages/DocumentDetail";
import Citations from "../pages/Citations";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/notes" element={<Notes />} />
          <Route path="/flashcards" element={<Flashcards />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/research" element={<Research />} />
          <Route path="/multi-chat" element={<MultiChat />} />
          <Route path="/citations" element={<Citations />} />
          <Route path="/documents/:id" element={<DocumentDetail />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}