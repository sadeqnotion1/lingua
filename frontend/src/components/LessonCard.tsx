// A single library card: cover, title, source, and a "new words" badge,
// mirroring the LingQ library tiles.
export interface LessonCardProps {
	title: string
	source?: string
	coverUrl?: string
	newWordsPct?: number
}

export default function LessonCard({ title, source, coverUrl, newWordsPct }: LessonCardProps) {
	return (
		<article className="lesson-card">
			<div className="lesson-cover" style={coverUrl ? { backgroundImage: `url(${coverUrl})` } : undefined} />
			<div className="lesson-body">
				<h3 className="lesson-title">{title}</h3>
				{newWordsPct != null && <span className="badge">{newWordsPct}% new words</span>}
				{source && <span className="lesson-source">{source}</span>}
			</div>
		</article>
	)
}
