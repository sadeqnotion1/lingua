import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import { api, ApiError, type ReaderText, type ReaderToken } from "../api/client"
import TermDrawer, {
	type DrawerWord,
	type SavedTerm,
} from "../components/TermDrawer"
import "../styles/reader.css"

// Reader screen — renders a text word-by-word from the server-enriched endpoint
// GET /api/reading/text/:id. Each word token already carries its term status.
// M6: clicking a word opens the TermDrawer; saving recolors every matching
// token live (no full reload).

type LoadState = "loading" | "ready" | "error" | "missing"

// Familiarity → CSS class. Mirrors Lute/LingQ status semantics:
//   null / 0 → new (untracked or unknown)  → strong highlight
//   1..4     → learning (4 fading levels)
//   5 / 99   → known / well-known           → no highlight
//   98       → ignored                      → muted, no highlight
function wordClass(status: number | null): string {
	if (status === null || status === 0) return "rdr-word rdr-new"
	if (status >= 1 && status <= 4) return `rdr-word rdr-learning rdr-l${status}`
	if (status === 98) return "rdr-word rdr-ignored"
	return "rdr-word rdr-known"
}

function statusLabel(status: number | null): string {
	if (status === null || status === 0) return "New word"
	if (status >= 1 && status <= 4) return `Learning · level ${status}`
	if (status === 98) return "Ignored"
	return "Known"
}

export default function Reader() {
	const { textId } = useParams()
	const id = Number(textId)

	const [data, setData] = useState<ReaderText | null>(null)
	const [state, setState] = useState<LoadState>("loading")
	const [selected, setSelected] = useState<DrawerWord | null>(null)

	useEffect(() => {
		let alive = true
		if (!Number.isFinite(id)) {
			setState("missing")
			return
		}
		setState("loading")
		api
			.getReaderText(id)
			.then((res) => {
				if (!alive) return
				setData(res)
				setState("ready")
			})
			.catch((err) => {
				if (!alive) return
				setState(
					err instanceof ApiError && err.status === 404 ? "missing" : "error",
				)
			})
		return () => {
			alive = false
		}
	}, [id])

	// Apply a saved term to every matching word token so the colour updates live.
	// Terms are case-insensitive within a language (D6), so we match on the
	// normalized surface form and refresh both status and term_id.
	function applySaved(saved: SavedTerm) {
		setData((prev) => {
			if (!prev) return prev
			return {
				...prev,
				tokens: prev.tokens.map((t) =>
					t.is_word && t.text.toLowerCase() === saved.text_lower
						? { ...t, status: saved.status, term_id: saved.term_id }
						: t,
				),
			}
		})
	}

	function openWord(tok: ReaderToken) {
		if (!data) return
		setSelected({
			text: tok.text,
			status: tok.status,
			termId: tok.term_id,
			languageId: data.language.id,
		})
	}

	return (
		<div className="reader-m5">
			<header className="rdr-bar">
				<Link to="/library" className="rdr-back">
					<BackIcon />
					<span>Library</span>
				</Link>
				<div className="rdr-bar-title">
					<span className="rdr-book">{data?.book_title ?? "\u00a0"}</span>
					{data && data.pagination.page_count > 1 && (
						<span className="rdr-page-count">
							Page {data.pagination.page_number} of {data.pagination.page_count}
						</span>
					)}
				</div>
				<div className="rdr-bar-spacer" aria-hidden="true" />
			</header>

			{state === "loading" && <ReaderSkeleton />}

			{state === "error" && (
				<div className="rdr-notice rdr-notice--error">
					<p>Couldn’t load this text.</p>
					<button
						type="button"
						className="rdr-btn"
						onClick={() => setState((s) => (s === "error" ? "loading" : s))}
					>
						Retry
					</button>
				</div>
			)}

			{state === "missing" && (
				<div className="rdr-notice">
					<p>That text doesn’t exist.</p>
					<Link to="/library" className="rdr-btn rdr-btn--primary">
						Back to library
					</Link>
				</div>
			)}

			{state === "ready" && data && (
				<>
					<article
						className="rdr-page"
						dir={data.language.right_to_left ? "rtl" : "ltr"}
					>
						{(data.title || data.book_title) && (
							<h1 className="rdr-title">{data.title || data.book_title}</h1>
						)}
						{data.tokens.length === 0 ? (
							<p className="rdr-empty">This page has no text yet.</p>
						) : (
							<p className="rdr-flow">
								{data.tokens.map((tok, i) => (
									<Token
										key={i}
										tok={tok}
										onSelect={() => openWord(tok)}
									/>
								))}
							</p>
						)}
					</article>

					<Legend />

					<nav className="rdr-nav" aria-label="Page navigation">
						<NavButton
							to={data.pagination.prev_text_id}
							dir="prev"
							label="Previous"
						/>
						<NavButton
							to={data.pagination.next_text_id}
							dir="next"
							label="Next"
						/>
					</nav>
				</>
			)}

			<TermDrawer
				word={selected}
				onClose={() => setSelected(null)}
				onSaved={applySaved}
			/>
		</div>
	)
}

function Token({
	tok,
	onSelect,
}: {
	tok: ReaderToken
	onSelect?: () => void
}) {
	if (!tok.is_word) {
		// Preserve spaces/punctuation/newlines exactly (container is pre-wrap).
		return <span className="rdr-punct">{tok.text}</span>
	}
	return (
		<span
			className={wordClass(tok.status)}
			title={statusLabel(tok.status)}
			role="button"
			tabIndex={0}
			onClick={onSelect}
			onKeyDown={(e) => {
				if (e.key === "Enter" || e.key === " ") {
					e.preventDefault()
					onSelect?.()
				}
			}}
		>
			{tok.text}
		</span>
	)
}

function NavButton({
	to,
	dir,
	label,
}: {
	to: number | null
	dir: "prev" | "next"
	label: string
}) {
	if (to === null) {
		return (
			<span className="rdr-btn rdr-btn--nav is-disabled" aria-disabled="true">
				{dir === "prev" && <ChevronIcon dir="prev" />}
				{label}
				{dir === "next" && <ChevronIcon dir="next" />}
			</span>
		)
	}
	return (
		<Link to={`/read/${to}`} className="rdr-btn rdr-btn--nav">
			{dir === "prev" && <ChevronIcon dir="prev" />}
			{label}
			{dir === "next" && <ChevronIcon dir="next" />}
		</Link>
	)
}

function Legend() {
	return (
		<div className="rdr-legend" aria-hidden="true">
			<span className="rdr-legend-item">
				<span className="rdr-word rdr-new">New</span>
			</span>
			<span className="rdr-legend-item">
				<span className="rdr-word rdr-learning rdr-l2">Learning</span>
			</span>
			<span className="rdr-legend-item">
				<span className="rdr-word rdr-known">Known</span>
			</span>
		</div>
	)
}

// Keep line skeleton width varied for realistic-looking load block.
function ReaderSkeleton() {
	return (
		<div className="rdr-page rdr-skel" aria-hidden="true">
			{[92, 78, 85, 64, 88, 72].map((w, i) => (
				<span className="rdr-skel-line" style={{ width: `${w}%` }} key={i} />
			))}
		</div>
	)
}

function BackIcon() {
	return (
		<svg
			width="18"
			height="18"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			strokeWidth="1.7"
			strokeLinecap="round"
			strokeLinejoin="round"
			aria-hidden="true"
		>
			<line x1="19" y1="12" x2="5" y2="12" />
			<polyline points="12 19 5 12 12 5" />
		</svg>
	)
}

function ChevronIcon({ dir }: { dir: "prev" | "next" }) {
	return (
		<svg
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			strokeWidth="1.8"
			strokeLinecap="round"
			strokeLinejoin="round"
			aria-hidden="true"
		>
			<polyline
				points={dir === "prev" ? "15 18 9 12 15 6" : "9 18 15 12 9 6"}
			/>
		</svg>
	)
}
