import { useEffect } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Library from "./pages/Library";
import Reader from "./pages/Reader";
import Account from "./pages/Account";
import Dashboard from "./pages/Dashboard";
import Search from "./pages/Search";
import Settings from "./pages/Settings";
import { applySavedAppearance, watchSystemTheme } from "./api/m8";
import "./styles/theme.css";

export default function App() {
  // Apply the saved theme/accent before first paint of real content so there
  // is no flash of the wrong theme, then keep "System" in sync with the OS.
  useEffect(() => {
    applySavedAppearance();
    return watchSystemTheme();
  }, []);

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/library" element={<Library />} />
          <Route path="/search" element={<Search />} />
          <Route path="/read/:textId" element={<Reader />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/account" element={<Account />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}
