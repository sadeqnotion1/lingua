import { Routes, Route, Navigate } from "react-router-dom"
import Sidebar from "./components/Sidebar"
import Library from "./pages/Library"
import Reader from "./pages/Reader"
import Account from "./pages/Account"

export default function App() {
	return (
		<div className="app-shell">
			<Sidebar />
			<main className="app-main">
				<Routes>
					<Route path="/" element={<Navigate to="/library" replace />} />
					<Route path="/library" element={<Library />} />
					<Route path="/read/:textId" element={<Reader />} />
					<Route path="/account" element={<Account />} />
				</Routes>
			</main>
		</div>
	)
}
