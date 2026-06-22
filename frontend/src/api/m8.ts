// M8 API client + appearance helpers (stats, search, settings).
//
// Self-contained on purpose: it reuses the same `/api` base + JSON conventions
// as api/client.ts WITHOUT importing its internals, so M8 stays additive and
// client.ts is untouched.

const BASE = "/api";

export class M8ApiError extends Error {
  status: number;
  body: unknown;
  constructor(status: number, body: unknown) {
    super(`Request failed with ${status}`);
    this.name = "M8ApiError";
    this.status = status;
    this.body = body;
  }
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) throw new M8ApiError(res.status, data);
  return data as T;
}

// ---- Stats ----
export interface StatusBreakdown {
  new: number;
  learning: number;
  known: number;
  well_known: number;
  ignored: number;
  total: number;
}
export interface StatsTotals {
  languages: number;
  books: number;
  texts: number;
  words: number;
  terms: number;
}
export interface LanguageStat {
  language_id: number | null;
  language_name: string;
  books: number;
  texts: number;
  words: number;
  terms: StatusBreakdown;
}
export interface Stats {
  totals: StatsTotals;
  terms: StatusBreakdown;
  languages: LanguageStat[];
}

// ---- Search ----
export interface BookHit {
  id: number;
  title: string;
  language_id: number | null;
  language_name: string | null;
  page_count: number;
}
export interface TextHit {
  text_id: number;
  title: string | null;
  book_id: number | null;
  book_title: string | null;
  page_number: number;
  language_name: string | null;
  snippet: string;
}
export interface TermHit {
  id: number;
  text: string;
  translation: string | null;
  status: number;
  language_id: number | null;
  language_name: string | null;
}
export interface SearchResults {
  query: string;
  books: BookHit[];
  texts: TextHit[];
  terms: TermHit[];
  total: number;
}

// ---- Settings ----
export interface Profile {
  username: string;
  email: string;
  tier: string;
  member_since: string | null;
}
export interface LanguageSetting {
  id: number;
  name: string;
  word_chars: string | null;
  right_to_left: boolean;
  show_romanization: boolean;
  book_count: number;
  term_count: number;
}
export interface LibraryTotals {
  languages: number;
  books: number;
  texts: number;
  terms: number;
}
export interface AppSettings {
  profile: Profile;
  preferences: Record<string, string>;
  languages: LanguageSetting[];
  totals: LibraryTotals;
}
export interface SettingsUpdate {
  profile?: { username?: string; email?: string };
  preferences?: Record<string, string>;
}
export interface LanguageSettingUpdate {
  word_chars?: string;
  right_to_left?: boolean;
  show_romanization?: boolean;
}

export const m8 = {
  getStats: () => req<Stats>("/stats"),
  search: (q: string) =>
    req<SearchResults>(`/search?q=${encodeURIComponent(q)}`),
  getSettings: () => req<AppSettings>("/settings"),
  updateSettings: (body: SettingsUpdate) =>
    req<AppSettings>("/settings", {
      method: "PUT",
      body: JSON.stringify(body),
    }),
  updateLanguage: (id: number, body: LanguageSettingUpdate) =>
    req<LanguageSetting>(`/settings/languages/${id}`, {
      method: "PUT",
      body: JSON.stringify(body),
    }),
};

// ---- Appearance (theme + accent) ----
// Persisted locally so the choice applies instantly on boot (before any fetch)
// and keeps working even if the API is momentarily unavailable.
const THEME_KEY = "linguaread:theme";
const ACCENT_KEY = "linguaread:accent";

export function applyTheme(theme: string): void {
  const root = document.documentElement;
  let resolved = theme;
  if (theme === "system") {
    resolved = window.matchMedia?.("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }
  root.dataset.theme = resolved;
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    /* ignore storage errors (private mode) */
  }
}

export function applyAccent(accent: string): void {
  if (!accent) return;
  document.documentElement.style.setProperty("--accent", accent);
  try {
    localStorage.setItem(ACCENT_KEY, accent);
  } catch {
    /* ignore storage errors */
  }
}

export function getSavedTheme(): string {
  try {
    return localStorage.getItem(THEME_KEY) || "system";
  } catch {
    return "system";
  }
}

export function getSavedAccent(): string {
  try {
    return localStorage.getItem(ACCENT_KEY) || "#2f80ed";
  } catch {
    return "#2f80ed";
  }
}

export function applySavedAppearance(): void {
  applyTheme(getSavedTheme());
  const accent = getSavedAccent();
  if (accent) applyAccent(accent);
}

export const STATUS_LABELS: Record<number, string> = {
  0: "New",
  1: "Learning 1",
  2: "Learning 2",
  3: "Learning 3",
  4: "Learning 4",
  5: "Known",
  98: "Ignored",
  99: "Well known",
};

export function statusLabel(status: number): string {
  return STATUS_LABELS[status] ?? "New";
}
