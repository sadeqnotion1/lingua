import { NavLink } from "react-router-dom"

// Left rail like the LingQ shell: Library / Reader / Account.
const links = [
	{ to: "/library", label: "Library" },
	{ to: "/account", label: "Account" },
]

export default function Sidebar() {
	return (
		<aside className="sidebar">
			<div className="brand">LinguaRead</div>
			<nav>
				{links.map((l) => (
					<NavLink key={l.to} to={l.to} className="nav-link">
						{l.label}
					</NavLink>
				))}
			</nav>
		</aside>
	)
}
