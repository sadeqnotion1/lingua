import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { m8, statusLabel, type SearchResults } from "../api/m8";
import "../styles/search.css";

/** Split text around the query (case-insensitive) and wrap matches in <mark>. */
function highlight(text: string, query: string) {
  if (!query) return text;
  const lower = text.toLowerCase();
  const q = query.toLowerCase();
  const out: (string | JSX.Element)[] = [];
  let i = 0;
  let key = 0;
  while (i < text.length) {
    const idx = lower.indexOf(q, i);
    if (idx < 0) {
      out.push(text.slice(i));
      break;
    }
    if (idx > i) out.push(text.slice(i, idx));
    out.push(<mark key={key++}>{text.slice(idx, idx + q.length)}</mark>);
    i = idx + q.length;
  }
  return out;
}

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const trimmed = query.trim();

  useEffect(() => {
    if (timer.current) clearTimeout(timer.current);
    if (!trimmed) {
      setResults(null);
      setError(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    timer.current = setTimeout(() => {
      m8.search(trimmed)
        .then((r) => {
          setResults(r);
          setError(null);
        })
        .catch((e) => setError(e?.message || "Search failed"))
        .finally(() => setLoading(false));
    }, 250);
    return () => {
      if (timer.current) clearTimeout(timer.current);
    };
  }, [trimmed]);

  const meta = useMemo(() => {
    if (!trimmed) return "Type to search books, pages and terms.";
    if (loading) return "Searching\u2026";
    if (error) return error;
    if (results)
      return `${results.total} result${results.total === 1 ? "" : "s"} for \u201c${results.query}\u201d`;
    return "";
  }, [trimmed, loading, error, results]);

  const hasAny = results && results.total > 0;

  return (
    <div className="srch">
      <h1>Search</h1>
      <div className="srch-box">
        <input
          className="srch-input"
          autoFocus
          placeholder="Search your library…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <div className="srch-meta">{meta}</div>

      {trimmed && !loading && !error && results && !hasAny && (
        <div className="srch-state">No matches. Try a different word.</div>
      )}

      {results && results.books.length > 0 && (
        <section className="srch-group">
          <h2>Books</h2>
          {results.books.map((b) => (
            <Link className="srch-hit" to="/library" key={`b${b.id}`}>
              <div className="title">{highlight(b.title, results.query)}</div>
              <div className="sub">
                {b.language_name ? `${b.language_name} \u00b7 ` : ""}
                {b.page_count} page{b.page_count === 1 ? "" : "s"}
              </div>
            </Link>
          ))}
        </section>
      )}

      {results && results.texts.length > 0 && (
        <section className="srch-group">
          <h2>Pages</h2>
          {results.texts.map((t) => (
            <Link
              className="srch-hit"
              to={`/read/${t.text_id}`}
              key={`t${t.text_id}`}
            >
              <div className="title">
                {highlight(
                  t.title || t.book_title || "Untitled",
                  results.query,
                )}
              </div>
              {t.snippet && (
                <div className="snippet">
                  {highlight(t.snippet, results.query)}
                </div>
              )}
              <div className="sub">
                {t.book_title ? `${t.book_title} \u00b7 ` : ""}page{" "}
                {t.page_number}
              </div>
            </Link>
          ))}
        </section>
      )}

      {results && results.terms.length > 0 && (
        <section className="srch-group">
          <h2>Terms</h2>
          {results.terms.map((t) => (
            <div className="srch-hit srch-term" key={`tm${t.id}`}>
              <span className="term-text">
                {highlight(t.text, results.query)}
              </span>
              {t.translation && (
                <span className="term-tr">
                  {highlight(t.translation, results.query)}
                </span>
              )}
              <span className="status-pill">{statusLabel(t.status)}</span>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}
