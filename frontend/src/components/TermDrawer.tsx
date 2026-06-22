import { useEffect, useRef, useState } from "react"
import { api, ApiError, type Term } from "../api/client"
import "../styles/term-drawer.css"

// TermDrawer (M6) — a sliding side panel for inspecting and editing a single
// term. Opens when a word token is clicked in the Reader. Handles both creating
// a brand-new term and updating an existing one (separate endpoints), then
// reports the saved status back so the Reader can recolor live.

export interface DrawerWord {
	text: string
	status: number | null
	termId: number | null
	languageId: number | null
}

export interface SavedTerm {
	term_id: number
	text_lower: string
	status: number
}

// The status choices offered in the UI. Matches the done-criteria set:
// 1-5, 98 (ignored), and 0 (new / reset). 99 is accepted by the API too but
// the reader renders it identically to "known", so we keep the picker simple.
const LEVELS: Array<{ value: number; label: string; hint: string }> = [
	{ value: 1, label: "1", hint: "Learning · new" },
	{ value: 2, label: "2", hint: "Learning" },
	{ value: 3, label: "3", hint: "Learning" },
	{ value: 4, label: "4", hint: "Learning · almost" },
	{ value: 5, label: "5", hint: "Known" },
]

function errorMessage(err: unknown): string {
	if (err instanceof ApiError) {
		const body = err.body as { detail?: unknown } | null
		const detail = body?.detail
		if (typeof detail === "string") return detail
		if (detail && typeof detail === "object" && "message" in detail) {
			return String((detail as { message: unknown }).message)
		}
		return `Couldn’t save (error ${err.status}).`
	}
	return "Couldn’t save. Check your connection and try again."
}

export default function TermDrawer({
	word,
	onClose,
	onSaved,
}: {
	word: DrawerWord | null
	onClose: () => void
	onSaved: (saved: SavedTerm) => void
}) {
	const open = word !== null

	const [status, setStatus] = useState<number>(0)
	const [translation, setTranslation] = useState<string>("")
	const [parentId, setParentId] = useState<string>("")
	const [loading, setLoading] = useState(false)
	const [saving, setSaving] = useState(false)
	const [error, setError] = useState<string | null>(null)

	const translationRef = useRef<HTMLInputElement>(null)

	// Hydrate the form whenever a new word is selected. For an existing term we
	// fetch its full details (translation + parent aren't carried on the token).
	useEffect(() => {
		if (!word) return
		let alive = true
		setError(null)
		setStatus(word.status ?? 0)
		setTranslation("")
		setParentId("")

		if (word.termId != null) {
			setLoading(true)
			api
				.getTerm(word.termId)
				.then((t) => {
					if (!alive) return
					setStatus(t.status)
					setTranslation(t.translation ?? "")
					setParentId(t.parent_id != null ? String(t.parent_id) : "")
				})
				.catch(() => {
					/* fall back to the token's status; editing still works */
				})
				.finally(() => {
					if (alive) setLoading(false)
				})
		}
		return () => {
			alive = false
		}
	}, [word])

	// Close on Escape; move focus into the panel when it opens.
	useEffect(() => {
		if (!open) return
		const onKey = (e: KeyboardEvent) => {
			if (e.key === "Escape") onClose()
		}
		window.addEventListener("keydown", onKey)
		const t = window.setTimeout(() => translationRef.current?.focus(), 60)
		return () => {
			window.removeEventListener("keydown", onKey)
			window.clearTimeout(t)
		}
	}, [open, onClose])

	async function persist(nextStatus: number) {
		if (!word) return
		if (word.languageId == null) {
			setError("This text has no language set, so terms can’t be saved.")
			return
		}
		setSaving(true)
		setError(null)
		const parsedParent =
			parentId.trim() === "" ? null : Number.parseInt(parentId.trim(), 10)
		if (parsedParent !== null && !Number.isFinite(parsedParent)) {
			setError("Parent term id must be a number.")
			setSaving(false)
			return
		}
		const trimmed = translation.trim()
		try {
			let saved: Term
			if (word.termId != null) {
				saved = await api.updateTerm(word.termId, {
					status: nextStatus,
					translation: trimmed === "" ? null : trimmed,
					parent_id: parsedParent,
				})
			} else {
				try {
					saved = await api.createTerm({
						text: word.text,
						language_id: word.languageId,
						status: nextStatus,
						translation: trimmed === "" ? null : trimmed,
						parent_id: parsedParent,
					})
				} catch (err) {
					// Term already exists (created elsewhere / stale token): the API
					// returns the existing row in the 409 body — switch to update.
					const existing = existingTermFrom409(err)
					if (!existing) throw err
					saved = await api.updateTerm(existing.id, {
						status: nextStatus,
						translation: trimmed === "" ? null : trimmed,
						parent_id: parsedParent,
					})
				}
			}
			onSaved({
				term_id: saved.id,
				text_lower: saved.text_lower,
				status: saved.status,
			})
			onClose()
		} catch (err) {
			setError(errorMessage(err))
		} finally {
			setSaving(false)
		}
	}

	return (
		<>
			<div
				className={`tdrawer-scrim ${open ? "is-open" : ""}`}
				onClick={onClose}
				aria-hidden="true"
			/>
			<aside
				className={`tdrawer ${open ? "is-open" : ""}`}
				role="dialog"
				aria-modal="true"
				aria-label="Term details"
				aria-hidden={open ? undefined : true}
			>
				{word && (
					<div className="tdrawer-inner">
						<header className="tdrawer-head">
							<div>
								<p className="tdrawer-kicker">
									{word.termId != null ? "Edit term" : "New term"}
								</p>
								<h2 className="tdrawer-word">{word.text}</h2>
							</div>
							<button
								type="button"
								className="tdrawer-close"
								onClick={onClose}
								aria-label="Close"
							>
								<CloseIcon />
							</button>
						</header>

						<section className="tdrawer-field">
							<span className="tdrawer-label">Familiarity</span>
							<div
								className="tdrawer-levels"
								role="group"
								aria-label="Familiarity level"
							>
								{LEVELS.map((lv) => (
									<button
										key={lv.value}
										type="button"
										className={`tdrawer-level tdrawer-l${lv.value} ${status === lv.value ? "is-active" : ""}`}
										aria-pressed={status === lv.value}
										title={lv.hint}
										disabled={saving}
										onClick={() => setStatus(lv.value)}
									>
										{lv.label}
									</button>
								))}
							</div>
							<div className="tdrawer-flags">
								<button
									type="button"
									className={`tdrawer-flag ${status === 98 ? "is-active" : ""}`}
									aria-pressed={status === 98}
									disabled={saving}
									onClick={() => setStatus(98)}
								>
									Ignore
								</button>
								<button
									type="button"
									className={`tdrawer-flag ${status === 0 ? "is-active" : ""}`}
									aria-pressed={status === 0}
									disabled={saving}
									onClick={() => setStatus(0)}
								>
									Reset
								</button>
							</div>
						</section>

						<label className="tdrawer-field">
							<span className="tdrawer-label">Translation</span>
							<input
								ref={translationRef}
								type="text"
								className="tdrawer-input"
								value={translation}
								placeholder={loading ? "Loading…" : "What does it mean?"}
								disabled={saving}
								onChange={(e) => setTranslation(e.target.value)}
							/>
						</label>

						<label className="tdrawer-field">
							<span className="tdrawer-label">Parent term id (optional)</span>
							<input
								type="text"
								inputMode="numeric"
								className="tdrawer-input"
								value={parentId}
								placeholder="Link to a root term by id"
								disabled={saving}
								onChange={(e) => setParentId(e.target.value)}
							/>
						</label>

						{error && <p className="tdrawer-error">{error}</p>}

						<div className="tdrawer-actions">
							<button
								type="button"
								className="tdrawer-btn tdrawer-btn--ghost"
								onClick={onClose}
								disabled={saving}
							>
								Cancel
							</button>
							<button
								type="button"
								className="tdrawer-btn tdrawer-btn--primary"
								onClick={() => persist(status)}
								disabled={saving}
							>
								{saving ? "Saving…" : "Save"}
							</button>
						</div>
					</div>
				)}
			</aside>
		</>
	)
}

function existingTermFrom409(err: unknown): Term | null {
	if (!(err instanceof ApiError) || err.status !== 409) return null
	const body = err.body as { detail?: { term?: Term } } | null
	const term = body?.detail?.term
	return term && typeof term.id === "number" ? term : null
}

function CloseIcon() {
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
			<line x1="18" y1="6" x2="6" y2="18" />
			<line x1="6" y1="6" x2="18" y2="18" />
		</svg>
	)
}
