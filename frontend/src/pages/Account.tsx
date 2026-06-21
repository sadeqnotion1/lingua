import { useEffect, useState } from "react"
import { api, Account as AccountData } from "../api/client"

// Account screen — mirrors the LingQ settings: username, email, password,
// plan/tier, and account stats. Stub data for now.
export default function Account() {
	const [account, setAccount] = useState<AccountData | null>(null)

	useEffect(() => {
		api.getAccount().then(setAccount).catch(() => setAccount(null))
	}, [])

	return (
		<div className="account">
			<h1>Account</h1>
			<form className="settings-form">
				<label>Username<input defaultValue={account?.username ?? ""} /></label>
				<label>Email<input defaultValue={account?.email ?? ""} /></label>
				<label>Password<input type="password" /></label>
				<label>Confirm Password<input type="password" /></label>
			</form>
			<dl className="account-meta">
				<dt>Current Tier</dt><dd>{account?.tier ?? "—"}</dd>
				<dt>Member Since</dt><dd>{account?.member_since ?? "—"}</dd>
			</dl>
		</div>
	)
}
