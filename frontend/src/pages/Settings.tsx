import { useEffect, useState } from "react";
import {
  applyAccent,
  applyTheme,
  m8,
  type AppSettings,
  type LanguageSetting,
} from "../api/m8";
import "../styles/settings.css";

const THEMES = [
  { value: "system", label: "System" },
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
];

// Features visible in the LingQ reference screen that are intentionally not part
// of this self-hosted, single-user build. Listed honestly rather than faked.
const UNAVAILABLE = [
  "Password / sign-in: no auth layer yet (single local user)",
  "Billing & plans: self-hosted, always the free tier",
  "Points, streaks & invites: no gamification/social layer",
  "Audio transcription: not wired up",
  "Delete account: single-user app; manage the SQLite file directly",
];

function LanguageCard({
  lang,
  onSaved,
}: {
  lang: LanguageSetting;
  onSaved: (updated: LanguageSetting) => void;
}) {
  const [wordChars, setWordChars] = useState(lang.word_chars || "");
  const [rtl, setRtl] = useState(lang.right_to_left);
  const [roman, setRoman] = useState(lang.show_romanization);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);

  function save() {
    setSaving(true);
    setMsg(null);
    m8.updateLanguage(lang.id, {
      word_chars: wordChars,
      right_to_left: rtl,
      show_romanization: roman,
    })
      .then((updated) => {
        setMsg({ ok: true, text: "Saved" });
        onSaved(updated);
      })
      .catch((e) => setMsg({ ok: false, text: e?.message || "Save failed" }))
      .finally(() => setSaving(false));
  }

  return (
    <div className="set-lang">
      <div className="lang-head">
        <span className="lang-name">{lang.name}</span>
        <span className="lang-meta">
          {lang.book_count} books · {lang.term_count} terms
        </span>
      </div>
      <div className="set-row">
        <label>Word characters (regex class used by the tokenizer)</label>
        <input
          className="set-input"
          value={wordChars}
          onChange={(e) => setWordChars(e.target.value)}
        />
      </div>
      <div className="set-checks">
        <label className="set-check">
          <input
            type="checkbox"
            checked={rtl}
            onChange={(e) => setRtl(e.target.checked)}
          />
          Right to left
        </label>
        <label className="set-check">
          <input
            type="checkbox"
            checked={roman}
            onChange={(e) => setRoman(e.target.checked)}
          />
          Show romanization
        </label>
      </div>
      <div className="set-inline">
        <button className="btn" onClick={save} disabled={saving}>
          {saving ? "Saving…" : "Save"}
        </button>
        {msg && (
          <span className={`set-msg ${msg.ok ? "ok" : "err"}`}>{msg.text}</span>
        )}
      </div>
    </div>
  );
}

export default function Settings() {
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Profile form.
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [profileMsg, setProfileMsg] = useState<{
    ok: boolean;
    text: string;
  } | null>(null);
  const [savingProfile, setSavingProfile] = useState(false);

  // Appearance.
  const [theme, setTheme] = useState("system");
  const [accent, setAccent] = useState("#2f80ed");

  function hydrate(s: AppSettings) {
    setSettings(s);
    setUsername(s.profile.username);
    setEmail(s.profile.email);
    setTheme(s.preferences.theme || "system");
    setAccent(s.preferences.accent || "#2f80ed");
  }

  function load() {
    setLoading(true);
    setError(null);
    m8.getSettings()
      .then(hydrate)
      .catch((e) => setError(e?.message || "Failed to load settings"))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  function saveProfile() {
    setSavingProfile(true);
    setProfileMsg(null);
    m8.updateSettings({ profile: { username, email } })
      .then((s) => {
        hydrate(s);
        setProfileMsg({ ok: true, text: "Saved" });
      })
      .catch((e) =>
        setProfileMsg({ ok: false, text: e?.message || "Save failed" }),
      )
      .finally(() => setSavingProfile(false));
  }

  function onThemeChange(value: string) {
    setTheme(value);
    applyTheme(value);
    m8.updateSettings({ preferences: { theme: value } }).catch(() => {});
  }

  function onAccentInput(value: string) {
    setAccent(value);
    applyAccent(value);
  }

  function saveAccent() {
    applyAccent(accent);
    m8.updateSettings({ preferences: { accent } }).catch(() => {});
  }

  function onLanguageSaved(updated: LanguageSetting) {
    setSettings((prev) =>
      prev
        ? {
            ...prev,
            languages: prev.languages.map((l) =>
              l.id === updated.id ? updated : l,
            ),
          }
        : prev,
    );
  }

  if (loading) {
    return (
      <div className="settings-m8">
        <div className="set-hint">Loading settings…</div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="settings-m8">
        <div className="set-card">
          <p className="set-msg err">{error}</p>
          <button className="btn btn-ghost" onClick={load}>
            Try again
          </button>
        </div>
      </div>
    );
  }
  if (!settings) return null;

  const { profile, totals, languages } = settings;

  const totalCards = [
    { num: totals.languages, label: "Languages" },
    { num: totals.books, label: "Total imports" },
    { num: totals.texts, label: "Pages" },
    { num: totals.terms, label: "Total terms" },
  ];

  return (
    <div className="settings-m8">
      <h1>Settings</h1>

      <section className="set-card">
        <h2>Profile</h2>
        <p className="set-hint">Your account details.</p>
        <div className="set-row">
          <label htmlFor="set-username">Username</label>
          <input
            id="set-username"
            className="set-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="set-row">
          <label htmlFor="set-email">Email</label>
          <input
            id="set-email"
            className="set-input"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="set-readonly">
          <div className="ro">
            <div className="num">{profile.tier.toUpperCase()}</div>
            <div className="lab">Current tier</div>
          </div>
          <div className="ro">
            <div className="num">{profile.member_since || "—"}</div>
            <div className="lab">Member since</div>
          </div>
        </div>
        <div className="set-inline">
          <button
            className="btn"
            onClick={saveProfile}
            disabled={savingProfile}
          >
            {savingProfile ? "Saving…" : "Save profile"}
          </button>
          {profileMsg && (
            <span className={`set-msg ${profileMsg.ok ? "ok" : "err"}`}>
              {profileMsg.text}
            </span>
          )}
        </div>
      </section>

      <section className="set-card">
        <h2>Appearance</h2>
        <p className="set-hint">
          Applies instantly and is remembered on this device.
        </p>
        <div className="set-row">
          <label htmlFor="set-theme">Theme</label>
          <select
            id="set-theme"
            className="set-select"
            value={theme}
            onChange={(e) => onThemeChange(e.target.value)}
          >
            {THEMES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>
        <div className="set-row">
          <label htmlFor="set-accent">Accent colour</label>
          <div className="set-inline">
            <input
              id="set-accent"
              className="set-swatch"
              type="color"
              value={accent}
              onChange={(e) => onAccentInput(e.target.value)}
            />
            <span className="set-hint">{accent}</span>
            <button className="btn btn-ghost" onClick={saveAccent}>
              Save colour
            </button>
          </div>
        </div>
      </section>

      <section className="set-card">
        <h2>Library</h2>
        <p className="set-hint">Live totals across your whole library.</p>
        <div className="set-readonly">
          {totalCards.map((c) => (
            <div className="ro" key={c.label}>
              <div className="num">{c.num.toLocaleString()}</div>
              <div className="lab">{c.label}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="set-card">
        <h2>Languages</h2>
        <p className="set-hint">
          These control how the reader tokenizes and displays each language.
        </p>
        {languages.length === 0 ? (
          <p className="set-hint">No languages yet.</p>
        ) : (
          languages.map((l) => (
            <LanguageCard key={l.id} lang={l} onSaved={onLanguageSaved} />
          ))
        )}
      </section>

      <section className="set-card">
        <h2>Not available in this build</h2>
        <p className="set-hint">
          Shown for transparency — these LingQ features are intentionally out of
          scope for a self-hosted, single-user app.
        </p>
        <ul className="set-unavailable">
          {UNAVAILABLE.map((u) => (
            <li key={u}>{u}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
