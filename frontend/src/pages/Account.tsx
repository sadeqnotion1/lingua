// Account screen — read-only profile for LinguaRead's single local user.
// Shows username, email, plan tier, and member-since, served by GET /api/account.
import { useEffect, useState } from "react";
import type { CSSProperties } from "react";
import { api, type Account } from "../api/client";
import "../styles/account.css";

const headStyle: CSSProperties = {
	display: "flex",
	alignItems: "center",
	gap: "0.75rem",
};

export default function Account() {
	const [account, setAccount] = useState<Account | null>(null);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		let active = true;
		api
			.getAccount()
			.then((data) => {
				if (active) setAccount(data);
			})
			.catch(() => {
				if (active)
					setError(
						"Couldn't load your account. Seed the local user first: python backend/tools/seed.py",
					);
			});
		return () => {
			active = false;
		};
	}, []);

	return (
		<div className="account">
			<div className="account__head" style={headStyle}>
				<h1>Account</h1>
				{account ? <span className="account__tier">{account.tier}</span> : null}
			</div>

			{error ? <p className="account__error">{error}</p> : null}

			<dl className="account__meta">
				<div className="account__row">
					<dt>Username</dt>
					<dd>{account?.username || "—"}</dd>
				</div>
				<div className="account__row">
					<dt>Email</dt>
					<dd>{account?.email || "—"}</dd>
				</div>
				<div className="account__row">
					<dt>Plan</dt>
					<dd>{account?.tier || "—"}</dd>
				</div>
				<div className="account__row">
					<dt>Member since</dt>
					<dd>{account?.member_since || "—"}</dd>
				</div>
			</dl>

			<p className="account__note">
				LinguaRead is single-user — this profile reflects your seeded local
				account.
			</p>
		</div>
	);
}
