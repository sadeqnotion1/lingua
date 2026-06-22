// Tiny fetch wrapper. In dev, Vite proxies /api -> FastAPI (port 8000).
// In production the backend serves this SPA, so /api is same-origin.

const BASE = "/api"

/** Error thrown for non-2xx API responses. Carries the HTTP status and the
 *  parsed response body (when present) so callers can render friendly messages
 *  — e.g. the 409 duplicate-book conflict from POST /api/library/import. */
export class ApiError extends Error {
	status: number
	body: unknown
	constructor(status: number, body: unknown, path: string) {
		super(`API ${status}: ${path}`)
		this.name = "ApiError"
		this.status = status
		this.body = body
	}
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE}${path}`, {
		headers: { "Content-Type": "application/json" },
		...init,
	})
	if (!res.ok) {
		let body: unknown = null
		try {
			body = await res.json()
		} catch {
			/* response had no JSON body */
		}
		throw new ApiError(res.status, body, path)
	}
	return res.json() as Promise<T>
}

/** A single library item as shown on a shelf (mirrors backend BookOut). */
export interface BookOut {
	id: number
	title: string
	source: string | null
	cover_url: string | null
	language_id: number | null
	page_count: number
}

/** Books grouped under one language — a "shelf" (mirrors backend LanguageGroup). */
export interface LanguageGroup {
	language_id: number | null
	language_name: string
	books: BookOut[]
}

/** Payload for POST /api/library/import. `language` accepts a name or an id. */
export interface ImportRequest {
	title: string
	text: string
	language?: string | number | null
}

/** Result of a successful import (mirrors backend ImportResponse). */
export interface ImportResponse {
	book: BookOut
	text_id: number
	created: boolean
}

/** One lossless token of a text (mirrors backend TokenOut). `status` is the
 *  matched term familiarity for word tokens, or null for a brand-new word. */
export interface ReaderToken {
	text: string
	is_word: boolean
	status: number | null
	term_id: number | null
}

export interface ReaderLanguage {
	id: number | null
	name: string | null
	right_to_left: boolean
}

export interface ReaderPagination {
	page_number: number
	page_count: number
	prev_text_id: number | null
	next_text_id: number | null
}

/** Everything the reader needs to render one text/page (mirrors backend ReaderText). */
export interface ReaderText {
	text_id: number
	title: string | null
	book_id: number | null
	book_title: string | null
	language: ReaderLanguage
	pagination: ReaderPagination
	tokens: ReaderToken[]
}

export const api = {
	health: () => request<{ status: string }>("/health"),
	listBooks: () => request<LanguageGroup[]>("/library/books"),
	importText: (payload: ImportRequest) =>
		request<ImportResponse>("/library/import", {
			method: "POST",
			body: JSON.stringify(payload),
		}),
	getReaderText: (textId: number) =>
		request<ReaderText>(`/reading/text/${textId}`),
	getAccount: () => request<Account>("/account"),
}

export interface Account {
	username: string
	email: string
	tier: string
	member_since: string | null
}
