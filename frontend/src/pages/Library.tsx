import { useEffect, useMemo, useState } from "react"
import { useSearchParams } from "react-router-dom"
import ShelfRow from "../components/ShelfRow"
import { api, ApiError, type LanguageGroup } from "../api/client"
import "../styles/library.css"

// Library screen (M3) — mirrors the LingQ library: a search + import bar on top,
// then one shelf per language with a card per book. Data comes from the real M2
// API (GET /api/library/books, POST /api/library/import) — nothing is mocked.

type LoadState = "loading" | "ready" | "error"

export default function Library() {
	// A book hit on the Search screen deep-links here as /library?q=<title>, so
	// seed the filter from the URL to land on (or near) that book.
	const [searchParams] = useSearchParams()
	const [groups, setGroups] = useState<LanguageGroup[]>([])
	const [loadState, setLoadState] = useState<LoadState>("loading")
	const [query, setQuery] = useState(() => searchParams.get("q") ?? "")
	const [importOpen, setImportOpen] = useState(false)

	// Import form state.
	const [title, setTitle] = useState("")
	const [language, setLanguage] = useState("")
	const [text, setText] = useState("")
	const [submitting, setSubmitting] = useState(false)
	const [formError, setFormError] = useState<string | null>(null)
	const [flash, setFlash] = useState<string | null>(null)

	async function load() {
		setLoadState("loading")
		try {
			const data = await api.listBooks()
			setGroups(data)
			setLoadState("ready")
		} catch {
			setLoadState("error")
		}
	}

	useEffect(() => {
		load()
	}, [])

	const knownLanguages = useMemo(
		() => Array.from(new Set(groups.map((g) => g.language_name))).sort(),
		[groups],
	)

	const totalBooks = useMemo(
		() => groups.reduce((n, g) => n + g.books.length, 0),
		[groups],
	)

	const filtered = useMemo(() => {
		const q = query.trim().toLowerCase()
		if (!q) return groups
		return groups
			.map((g) => ({
				...g,
				books: g.books.filter(
					(b) =>
						b.title.toLowerCase().includes(q) ||
						(b.source ?? "").toLowerCase().includes(q),
				),
			}))
			.filter((g) => g.books.length > 0)
	}, [groups, query])

	async function onImport(e: React.FormEvent<HTMLFormElement>) {
		e.preventDefault()
		setFormError(null)
		if (!title.trim() || !text.trim()) {
			setFormError("Both a title and some text are required.")
			return
		}
		setSubmitting(true)
		try {
			const langValue = language.trim() ? language.trim() : undefined
			const res = await api.importText({
				title: title.trim(),
				text,
				language: langValue,
			})
			setTitle("")
			setLanguage("")
			setText("")
			setImportOpen(false)
			setFlash(`Imported “${res.book.title}”.`)
			await load()
			window.setTimeout(() => setFlash(null), 3500)
		} catch (err) {
			setFormError(messageForError(err))
		} finally {
			setSubmitting(false)
		}
	}

	return (
		<div className="lib3">
			<div className="lib3__bar">
				<div className="lib3__title-wrap">
					<h1 className="lib3__heading">Library</h1>
					<p className="lib3__sub">
						{totalBooks} {totalBooks === 1 ? "book" : "books"} · {groups.length}{" "}
						{groups.length === 1 ? "language" : "languages"}
					</p>
				</div>
				<div className="lib3__bar-actions">
					<div className="lib3__search">
						<SearchIcon />
						<input
							type="search"
							value={query}
							onChange={(e) => setQuery(e.target.value)}
							placeholder="Search library"
							aria-label="Search library"
						/>
					</div>
					<button
						type="button"
						className="lib3__import-btn"
						onClick={() => setImportOpen((v) => !v)}
						aria-expanded={importOpen}
					>
						<PlusIcon />
						Import text
					</button>
				</div>
			</div>

			{flash && (
				<div className="lib3__flash" role="status">
					{flash}
				</div>
			)}

			{importOpen && (
				<form className="lib3__import" onSubmit={onImport} noValidate>
					<div className="lib3__import-grid">
						<label className="lib3__field">
							<span>Title</span>
							<input
								value={title}
								onChange={(e) => setTitle(e.target.value)}
								placeholder="e.g. The Little Prince — Ch.1"
								required
							/>
						</label>
						<label className="lib3__field">
							<span>Language</span>
							<input
								value={language}
								onChange={(e) => setLanguage(e.target.value)}
								placeholder="English"
								list="lib3-langs"
							/>
							<datalist id="lib3-langs">
								{knownLanguages.map((l) => (
									<option key={l} value={l} />
								))}
							</datalist>
						</label>
					</div>
					<label className="lib3__field">
						<span>Text</span>
						<textarea
							value={text}
							onChange={(e) => setText(e.target.value)}
							placeholder="Paste the text you want to read and study…"
							rows={7}
							required
						/>
					</label>
					{formError && (
						<p className="lib3__error" role="alert">
							{formError}
						</p>
					)}
					<div className="lib3__import-foot">
						<span className="lib3__hint">
							Leave language blank to default to English.
						</span>
						<div className="lib3__import-buttons">
							<button
								type="button"
								className="lib3__btn-ghost"
								onClick={() => setImportOpen(false)}
								disabled={submitting}
							>
								Cancel
							</button>
							<button
								type="submit"
								className="lib3__btn-primary"
								disabled={submitting}
							>
								{submitting ? "Importing…" : "Import"}
							</button>
						</div>
					</div>
				</form>
			)}

			{loadState === "loading" && <ShelvesSkeleton />}

			{loadState === "error" && (
				<div className="lib3__notice lib3__notice--error">
					<p>Couldn’t load your library.</p>
					<button className="lib3__btn-ghost" onClick={load} type="button">
						Retry
					</button>
				</div>
			)}

			{loadState === "ready" && filtered.length === 0 && (
				<div className="lib3__notice">
					{query.trim() ? (
						<p>No books match “{query.trim()}”.</p>
					) : (
						<>
							<p>Your library is empty.</p>
							<button
								className="lib3__btn-primary"
								type="button"
								onClick={() => setImportOpen(true)}
							>
								Import your first text
							</button>
						</>
					)}
				</div>
			)}

			{loadState === "ready" &&
				filtered.map((g) => (
					<ShelfRow
						key={g.language_id ?? g.language_name}
						title={g.language_name}
						books={g.books}
					/>
				))}
		</div>
	)
}

function messageForError(err: unknown): string {
	if (err instanceof ApiError) {
		const body = err.body as
			| { detail?: { message?: string } | string; message?: string }
			| null
		if (err.status === 409) {
			const detail = body?.detail
			const msg =
				detail && typeof detail === "object" && detail.message
					? detail.message
					: typeof body?.message === "string"
						? body.message
						: undefined
			return msg ?? "A book with this title already exists in that language."
		}
		if (err.status === 404) return "That language could not be found."
		if (err.status === 422) return "Please provide a valid title and text."
		return "Import failed. Please try again."
	}
	return "Network error — is the backend running on :8000?"
}

function SearchIcon() {
	return (
		<svg
			width="18"
			height="18"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			strokeWidth="1.6"
			strokeLinecap="round"
			strokeLinejoin="round"
			aria-hidden="true"
		>
			<circle cx="11" cy="11" r="7" />
			<line x1="21" y1="21" x2="16.65" y2="16.65" />
		</svg>
	)
}

function PlusIcon() {
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
			<line x1="12" y1="5" x2="12" y2="19" />
			<line x1="5" y1="12" x2="19" y2="12" />
		</svg>
	)
}

function ShelvesSkeleton() {
	return (
		<div className="lib3__skeleton" aria-hidden="true">
			{[0, 1].map((r) => (
				<section className="lib3-shelf" key={r}>
					<div className="lib3-shelf__head">
						<div className="lib3-skel lib3-skel--title" />
					</div>
					<div className="lib3-shelf__row">
						{[0, 1, 2, 3].map((c) => (
							<div className="lib3-skel lib3-skel--card" key={c} />
						))}
					</div>
				</section>
			))}
		</div>
	)
}
