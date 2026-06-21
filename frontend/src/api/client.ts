// Tiny fetch wrapper. In dev, Vite proxies /api -> FastAPI (port 8000).
// In production the backend serves this SPA, so /api is same-origin.

const BASE = "/api"

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE}${path}`, {
		headers: { "Content-Type": "application/json" },
		...init,
	})
	if (!res.ok) throw new Error(`API ${res.status}: ${path}`)
	return res.json() as Promise<T>
}

export const api = {
	health: () => request<{ status: string }>("/health"),
	listBooks: () => request<unknown[]>("/library/books"),
	getAccount: () => request<Account>("/account"),
}

export interface Account {
	username: string
	email: string
	tier: string
	member_since: string | null
}
