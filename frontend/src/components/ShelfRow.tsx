import { useRef } from "react"
import LessonCard from "./LessonCard"
import type { BookOut } from "../api/client"

// A horizontal "shelf" of lesson cards for one language, LingQ-style: a bold
// title with a chevron, a count on the right, and a scrollable row of cards
// with real prev/next arrow buttons.
export interface ShelfRowProps {
	title: string
	books: BookOut[]
}

function Chevron() {
	return (
		<svg
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			strokeWidth="2"
			strokeLinecap="round"
			strokeLinejoin="round"
			aria-hidden="true"
		>
			<polyline points="9 6 15 12 9 18" />
		</svg>
	)
}

export default function ShelfRow({ title, books }: ShelfRowProps) {
	const rowRef = useRef<HTMLDivElement>(null)

	function scroll(dir: -1 | 1) {
		const el = rowRef.current
		if (!el) return
		el.scrollBy({ left: dir * Math.round(el.clientWidth * 0.85), behavior: "smooth" })
	}

	const scrollable = books.length > 1

	return (
		<section className="lib3-shelf">
			<div className="lib3-shelf__head">
				<h2 className="lib3-shelf__title">
					{title}
					<span className="lib3-shelf__chev" aria-hidden="true">
						<Chevron />
					</span>
				</h2>
				<span className="lib3-shelf__count">
					{books.length} {books.length === 1 ? "book" : "books"}
				</span>
			</div>
			<div className="lib3-shelf__viewport">
				{scrollable && (
					<button
						type="button"
						className="lib3-shelf__nav lib3-shelf__nav--prev"
						onClick={() => scroll(-1)}
						aria-label={`Scroll ${title} left`}
					>
						<span className="lib3-shelf__nav-flip">
							<Chevron />
						</span>
					</button>
				)}
				<div className="lib3-shelf__row" ref={rowRef} role="list">
					{books.length === 0 ? (
						<p className="lib3-empty">No books on this shelf yet.</p>
					) : (
						books.map((b) => (
							<div role="listitem" key={b.id}>
								<LessonCard
									title={b.title}
								source={b.source}
								coverUrl={b.cover_url}
								pageCount={b.page_count}
							/>
							</div>
						))
					)}
				</div>
				{scrollable && (
					<button
						type="button"
						className="lib3-shelf__nav lib3-shelf__nav--next"
						onClick={() => scroll(1)}
						aria-label={`Scroll ${title} right`}
					>
						<Chevron />
					</button>
				)}
			</div>
		</section>
	)
}
