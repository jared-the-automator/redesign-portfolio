# Getting dugovic.com live on Render — the "just do what I say" guide

Read top to bottom. Don't skip ahead. Each step says what to click and what
you should see after you do it. Total time: about 15–20 minutes, most of it
waiting for things to finish in the background.

You'll need:
- A computer with a web browser (Chrome or Safari is fine).
- Your **GitHub** account (you're already on it — the site's files live in a
  GitHub repo you can open at:
  https://github.com/jared-the-automator/redesign-portfolio).
- Your **domain** login (where `dugovic.com` is registered — most likely
  GoDaddy, since Weebly is a GoDaddy company). You'll need this in Step 4.

We are NOT moving the domain registration anywhere. We are just telling the
domain where to send visitors. The domain stays registered where it is today.

---

## Part 1 — Put the website on Render

Render is the free website-hosting service that will serve the files.

1. Go to **https://render.com** in your browser.
2. Click **Sign In** (top right). Log in with the account *you* (Peter) use —
   NOT Jared's account. If you don't have an account yet, click **Sign Up**
   and make one (a free "Hobby" account is all you need).
3. After you log in you'll see a big blue button that says **New** in the
   upper-right. Click it. A small menu drops down.
4. In that menu, click **Blueprint**.
   - If you don't see "Blueprint," look for **New → Blueprints**. The option
     is there even on free accounts.
5. A screen titled something like **"Deploy a Blueprint"** appears with a box
   that says **Connect a repository**.
   - Make sure the GitHub icon is selected (not GitLab / Bitbucket).
   - If GitHub asks you to "Authorize" or "Install app," say **Yes /
     Authorize**. This just lets Render read your repos.
6. Find the repo named **redesign-portfolio** (owner: jared-the-automator).
   It's public, so it will be visible right away. Click it to select it.
   - The branch should say **main** — leave it as is.
7. Click **Continue** (or **Create Blueprint**).
   - A page will list what's about to be created. You should see one item:
     a static site named **dugovic**, with the domains
     `dugovic.com` and `www.dugovic.com`.
   - Read the "Estimated monthly cost." For a static site this should show
     **$0.00**. If it's not $0, stop and message Jared before continuing.
8. Click **Approve & Deploy** (a blue button, usually bottom of the page).
9. You'll see a green/white "deploying" screen with little steps lighting up.
   - **Do nothing here.** It runs automatically. This takes 1–3 minutes.
   - When it's done, the item turns green and shows a URL like
     `something.onrender.com`.
10. Open that `...onrender.com` URL in a new tab. **This is the moment of
    truth:** if the new dugovic site loads, Render is working. (The domain
    `dugovic.com` still won't work yet — that's the next part.)

> **You're halfway done.** The website now exists on Render. The
> `dugovic.com` address just isn't pointing at it yet.

---

## Part 2 — Point `dugovic.com` at Render

This is where the domain learns to send visitors to the new site instead of
the old Weebly site. We do it in **two places**: (a) add the domain to
Render, then (b) tell your domain registrar (GoDaddy) to point there.

### 2a. Tell Render which domain to use
1. Back in the **Render dashboard**, click on your **dugovic** site (the
   green one from Part 1).
2. Click the **Settings** tab (top of the page).
3. Scroll down to the **Custom Domains** section.
   - You should already see `dugovic.com` and `www.dugovic.com` listed (they
     came in with the Blueprint). If you do **not** see them, click
     **+ Add Custom Domain**, type `dugovic.com`, and save. Render will also
     add `www.dugovic.com` automatically.
4. Next to `dugovic.com` there's a status that says something like
   **"DNS update needed."** Keep this page open — you'll come back to it.
5. **Copy the exact address Render shows** for this site. It looks like
   `dugovic.onrender.com` or similar. **Save it somewhere** (a text file is
   fine). You'll type it in a moment. (It's the "value" for the `www` record
   in the next step.)

### 2b. Edit the DNS records at your registrar (GoDaddy)
DNS records are just "signposts" that tell the internet where a domain goes.
You're replacing the signposts that pointed to Weebly with ones that point
to Render.

1. Log in to wherever `dugovic.com` is registered (GoDaddy most likely:
   **godaddy.com**).
2. Find the domain **dugovic.com** and open its **DNS** settings.
   - On GoDaddy: click the domain → **DNS** (or "DNS Management").
   - If you're actually on Weebly's domain manager instead, the same two
     record types exist there; the button names just look slightly different.
3. In the list of records you'll see rows like `A`, `CNAME`, maybe `AAAA`.
   Look for any rows that point to **Weebly** (they may contain
   `weebly`, `editmysite`, or an IP you don't recognize).
   - **Delete** those `A` and `CNAME` rows (there's usually a **Delete** /
     trash icon on each row).
   - **Delete any `AAAA` record too.** (Render is IPv4-only; a leftover
     `AAAA` record will break the site.)
4. Now **add** these two records (click **Add New Record** / **+ Add record**):

   | Type | Name/Host | Value / Points to | TTL |
   |------|-----------|-------------------|-----|
   | `A`  | `@` (or leave Name blank) | `216.24.57.1` | 1 minute (or 3600) |
   | `CNAME` | `www` | `dugovic.onrender.com` ← use YOUR saved address from 2a.5 | 1 minute |

   Notes on typing these in:
   - **Name/Host**: for the `A` record type `@` (it means "the main domain").
     For the `CNAME` record type `www`.
   - **Value / Points to / Destination**: paste the exact value in the table.
     For the `CNAME`, it must be the `...onrender.com` address you saved in
     2a.5 — not `dugovic.com`.
   - **TTL**: choose the smallest available (1 minute / 3600). It just makes
     changes apply faster.
5. **Save** all changes.

> If GoDaddy shows a popup asking about "domain forwarding" or "website
> builder," **cancel it / say no** — we're not using forwarding, we're doing
> DNS records.

### 2c. Tell Render the DNS is set
1. Go back to the **Render → Settings → Custom Domains** page you kept open.
2. Next to `dugovic.com`, click **Verify** (you may need to refresh the page
   first).
3. Repeat for `www.dugovic.com` if it has its own Verify button.
4. This can take anywhere from a few minutes to ~30 minutes (DNS changes
   "propagate" across the internet). If it says "not found yet," wait 5
   minutes and hit **Verify** again.
5. When a domain shows **Verified** / a green check, Render has issued a free
   SSL certificate (that's the little lock 🔒 that makes the URL say
   `https://`).

---

## Part 3 — Prove it works and retire the old site

1. Open a **new, incognito/private browser window** (this avoids your old
   cached pages).
2. Go to **https://dugovic.com**. The new site should load.
   - Try **https://www.dugovic.com** too — it should either work or bounce
     you to the non-`www` version.
3. Walk through the site: Home, Works (click a category), About, Studio,
   Contact. Check the slideshow and that links open.
4. **Only after it looks right**, go back to Weebly and **cancel / delete the
   old site** so nobody pays for two things. (If you're nervous, you can
   leave Weebly running for a week; once you've confirmed the new site is
   solid, shut it off.)
5. **Do NOT cancel the domain registration** — you only cancelled the
   Weebly *website*. Keep paying for `dugovic.com` where you always have.

---

## If something goes wrong

- **The `...onrender.com` URL from Part 1 works, but `dugovic.com` doesn't:**
  The DNS in Part 2 hasn't fully propagated or a record was typed wrong.
  Re-check the two records against the table in 2b.4. Confirm the `A` record
  value is exactly `216.24.57.1`.
- **`dugovic.com` loads the OLD Weebly site:** You didn't delete the old
  Weebly/`editmysite` record, or propagation is incomplete. Make sure no
  record still points to Weebly, then wait and re-check.
- **You get a 502 / "bad gateway" right after verifying:** Render is still
  wiring up routing. Wait a few minutes and reload.
- **It asks for money / cost isn't $0:** Stop and message Jared before you
  confirm.
- **You see a login screen or "not found" on the site itself** (not a DNS
  error): The site files didn't deploy. In Render, open the site → **Logs**,
  look for a red error, and send that screenshot to Jared.

## What NOT to do
- Don't "transfer the domain into Render" unless we specifically ask — we're
  intentionally keeping the registration at your current registrar.
- Don't type a `CNAME` for the `@`/root record (only `www` gets a CNAME).
- Don't delete the `AAAA` record until after the new `A` record is in place,
  or the site will be unreachable for a moment.
- Don't turn off Weebly until Step 3.2 above is confirmed.

---
*Technical reference version: see `DEPLOY.md` (same folder) if you want the
short version without the hand-holding.*
