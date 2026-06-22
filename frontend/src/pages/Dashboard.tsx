import { useEffect, useState } from "react";
import { m8, type Stats, type StatusBreakdown } from "../api/m8";
import "../styles/dashboard.css";

const SEGMENTS: { key: keyof StatusBreakdown; cls: string; label: string }[] = [
  { key: "new", cls: "seg-new", label: "New" },
  { key: "learning", cls: "seg-learning", label: "Learning" },
  { key: "known", cls: "seg-known", label: "Known" },
  { key: "well_known", cls: "seg-well_known", label: "Well known" },
  { key: "ignored", cls: "seg-ignored", label: "Ignored" },
];

function StatusBar({ b }: { b: StatusBreakdown }) {
  const total = b.total || 0;
  return (
    <div
      className="dash-bar"
      role="img"
      aria-label="Vocabulary status breakdown"
    >
      {total > 0 &&
        SEGMENTS.map((s) => {
          const v = b[s.key];
          if (!v) return null;
          return (
            <span
              key={s.key}
              className={s.cls}
              style={{ width: `${(v / total) * 100}%` }}
              title={`${s.label}: ${v}`}
            />
          );
        })}
    </div>
  );
}

function Legend({ b }: { b: StatusBreakdown }) {
  return (
    <div className="dash-legend">
      {SEGMENTS.map((s) => (
        <span className="leg" key={s.key}>
          <span className={`dot ${s.cls}`} />
          {s.label} <span className="cnt">{b[s.key]}</span>
        </span>
      ))}
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  function load() {
    setLoading(true);
    setError(null);
    m8.getStats()
      .then(setStats)
      .catch((e) => setError(e?.message || "Failed to load stats"))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) {
    return (
      <div className="dash">
        <div className="dash-state">Loading dashboard…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dash">
        <div className="dash-state">
          <div>{error}</div>
          <button className="dash-retry" onClick={load}>
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  const { totals, terms, languages } = stats;
  const empty = totals.books === 0 && totals.terms === 0;

  const cards = [
    { num: totals.languages, label: "Languages" },
    { num: totals.books, label: "Books" },
    { num: totals.texts, label: "Pages" },
    { num: totals.words, label: "Words" },
    { num: totals.terms, label: "Terms" },
  ];

  return (
    <div className="dash">
      <h1>Dashboard</h1>
      <p className="dash-sub">Your reading and vocabulary at a glance.</p>

      {empty ? (
        <div className="dash-state">
          Nothing here yet. Import a text from the Library to get started.
        </div>
      ) : (
        <>
          <div className="dash-cards">
            {cards.map((c) => (
              <div className="dash-card" key={c.label}>
                <div className="num">{c.num.toLocaleString()}</div>
                <div className="label">{c.label}</div>
              </div>
            ))}
          </div>

          <div className="dash-section">
            <h2>Vocabulary ({terms.total.toLocaleString()} terms)</h2>
            <StatusBar b={terms} />
            <Legend b={terms} />
          </div>

          {languages.length > 0 && (
            <div className="dash-section">
              <h2>By language</h2>
              <div className="dash-langs">
                {languages.map((l) => (
                  <div
                    className="dash-lang"
                    key={l.language_id ?? l.language_name}
                  >
                    <div className="lang-head">
                      <span className="lang-name">{l.language_name}</span>
                      <span className="lang-meta">
                        {l.books} books · {l.words.toLocaleString()} words
                      </span>
                    </div>
                    <StatusBar b={l.terms} />
                    <Legend b={l.terms} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
