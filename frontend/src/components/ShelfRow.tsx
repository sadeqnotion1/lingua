import LessonCard, { LessonCardProps } from "./LessonCard"

// A horizontal "shelf" (e.g. Continue Studying, For You, Mini Stories) like LingQ.
export interface ShelfRowProps {
	title: string
	items: LessonCardProps[]
}

export default function ShelfRow({ title, items }: ShelfRowProps) {
	return (
		<section className="shelf">
			<div className="shelf-head">
				<h2>{title}</h2>
				<button className="shelf-viewall">View all</button>
			</div>
			<div className="shelf-row">
				{items.length === 0 ? (
					<p className="empty">No items yet.</p>
				) : (
					items.map((it, i) => <LessonCard key={i} {...it} />)
				)}
			</div>
		</section>
	)
}
