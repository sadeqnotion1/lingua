# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M7 — Account page.** Implement the account settings screen. This includes matching the layout and design of screenshot 2, letting the user view and edit their profile settings (username, email, password updates), and updating the backend account endpoints if needed to store/verify modifications.

## Start the next chat with this
> "Let's build M7 (Account page). Pull the backend account router and frontend account page so we can wire up user profile and settings management."

## What to paste / give me at the start
Pull these from the repo:
1. `backend/app/routers/account.py` (the router for account API calls)
2. `frontend/src/pages/Account.tsx` (the React page for settings and profile form)

## Decisions I need from you for M7
- Profile Persistence: Should settings updates be stored in the SQLite database (e.g., adding a User/Account model), or are we keeping it as stub data/settings configurations?
- Authentication: Should we introduce password change validation/hashing or keep the stub authentication model?

## Definition of done for this task
- The Account settings screen matches the design references and layout.
- The user can view profile fields (username, email, plan tier, member since) and input updates.
- Profile changes are correctly processed and saved.
- All type-safety checks and backend/frontend unit tests pass cleanly.
