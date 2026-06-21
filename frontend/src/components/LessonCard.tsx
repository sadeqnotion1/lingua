// A single library card in the LingQ light style: a landscape cover with an
// overlaid count badge, then title + source below. Bound to REAL backend data
// only (title, source, cover_url, page_count) — no fabricated "% new words",
// likes, or progress (those don't exist server-side until M5 Reader / M6 Terms).
export interface LessonCardProps {
	title: string
	source?: string | null
	coverUrl?: string | null
	pageCount?: number
	languageName?: string
}

function initials(title: string): string {
	const t = title.trim()
	if (!t) return "?"
	const parts = t.split(/\s+/).slice(0, 2)
	const joined = parts.map((p) => p[0]?.toUpperCase() ?? "").join("")
	return joined || t[0].toUpperCase()
}

function PagesIcon() {
	return (
		<svg
			width="13"
			height="13"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			strokeWidth="1.7"
			strokeLinecap="round"
			strokeLinejoin="round"
			aria-hidden="true"
		>
			<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5z" />
			<path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5z" />
		</svg>
	)
}

export default function LessonCard({
	title,
	source,
	coverUrl,
	pageCount,
	languageName,
}: LessonCardProps) {
	const pages = pageCount ?? 0
	return (
		<article className="lib3-card" tabIndex={0} aria-label={title}>
			<div
				className="lib3-card__cover"
				style={coverUrl ? { backgroundImage: `url(${coverUrl})` } : undefined}
			>
				{!coverUrl && (
					<span className="lib3-card__placeholder" aria-hidden="true">
						{initials(title)}
					</span>
				)}
				{languageName && <span className="lib3-card__lang">{languageName}</span>}
				<div className="lib3-card__badges">
					<span
						className="lib3-badge"
						title={`${pages} ${pages === 1 ? "page" : "pages"}`}
					>
						<PagesIcon />
						{pages}
					</span>
				</div>
			</div>
			<div className="lib3-card__body">
				<h3 className="lib3-card__title">{title}</h3>
				{source && (
					<span className="lib3-card__source" title={source}>
						{source}
					</span>
				)}
			</div>
		</article>
	)
}
