import { useParams } from "react-router-dom"

// Reader screen — where text renders word-by-word with click-to-define.
// The core LingQ/Lute interaction lives here (to be implemented).
export default function Reader() {
	const { textId } = useParams()
	return (
		<div className="reader">
			<h1>Reader</h1>
			<p className="muted">Text #{textId} — tokenized reading view goes here.</p>
			<div className="reader-pane">
				<p>Click a word to look it up and set its status.</p>
			</div>
		</div>
	)
}
