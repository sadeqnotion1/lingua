// Account screen (M7) — read-only profile backed by GET /api/account.
// Editing + password change arrive with authentication (a later milestone),
// so we intentionally do NOT render fake editable fields here.
import { useEffect, useState } from "react";
import { api } from "../api/client";
import "../styles/account.css";

type AccountInfo = {
  username: string;
  email: string;
  tier: string;
  member_since: string | null;
};

export default function Account() {
  const [account, setAccount] = useState<AccountInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getAccount()
      .then((data) => setAccount(data as AccountInfo))
      .catch(() =>
        setError("Couldn't load your account. Have you seeded a user yet?"),
      );
  }, []);

  const initial = (account?.username ?? "?").slice(0, 1).toUpperCase();

  return (
    <div className="account">
      <header className="account__head">
        <div className="account__avatar" aria-hidden="true">
          {initial}
        </div>
        <div>
          <h1 className="account__name">{account?.username ?? "\u2014"}</h1>
          <p className="account__email">{account?.email ?? "\u2014"}</p>
        </div>
        {account?.tier ? (
          <span className="account__tier">{account.tier}</span>
        ) : null}
      </header>

      {error ? <p className="account__error">{error}</p> : null}

      <dl className="account__meta">
        <div className="account__row">
          <dt>Username</dt>
          <dd>{account?.username ?? "\u2014"}</dd>
        </div>
        <div className="account__row">
          <dt>Email</dt>
          <dd>{account?.email ?? "\u2014"}</dd>
        </div>
        <div className="account__row">
          <dt>Current tier</dt>
          <dd>{account?.tier ?? "\u2014"}</dd>
        </div>
        <div className="account__row">
          <dt>Member since</dt>
          <dd>{account?.member_since ?? "\u2014"}</dd>
        </div>
      </dl>

      <p className="account__note">
        Profile editing &amp; password change arrive with authentication (a
        later milestone).
      </p>
    </div>
  );
}
