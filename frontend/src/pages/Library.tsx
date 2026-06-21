import { useEffect, useState } from "react"
import ShelfRow from "../components/ShelfRow"
import { api } from "../api/client"

// Library screen — mirrors the LingQ library: search + import bar, then shelves
// (Continue Studying, For You, Mini Stories, ...). Stub data for now.
export default function Library() {
	const [, setLoaded] = useState(false)

	useEffect(() => {
		api.listBooks().then(() => setLoaded(true)).catch(() => setLoaded(true))
	}, [])

	return (
		<div className="library">
			<header className="library-head">
				<input className="search" placeholder="Search Library" />
				<button className="import-btn">Import</button>
			</header>

			<ShelfRow title="Continue Studying" items={[]} />
			<ShelfRow title="For You" items={[]} />
			<ShelfRow title="Mini Stories" items={[]} />
		</div>
	)
}
