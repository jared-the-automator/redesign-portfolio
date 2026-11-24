# Getting dugovic.com live on Render — the "just do what I say" guide

Read top to bottom. Don't skip ahead. Each step says what to click and what
you should see after you do it. Total time: about 15–20 minutes, most of it
waiting for things to finish in the background.

You'll need:
- A computer with a web browser (Chrome or Safari is fine).
- The site's files live in a public GitHub repo:
  https://github.com/jared-the-automator/redesign-portfolio
  You do **not** need a GitHub account or login for the Render steps —
  the repo is public and you just paste its address into Render.
- Your **domain** login (where `dugovic.com` is registered). The domain's
  DNS is currently on GoDaddy nameservers, so you'll manage it at GoDaddy.
  You'll need this in Part 2.

We are NOT moving the domain registration anywhere. We are just telling the
domain where to send visitors. The domain stays registered where it is today.

---

## Part 1 — Put the website on Render

Render is the free website-hosting service that will serve the files.

1. Go to **https://render.com** in your browser.
2. Click **Sign In** (top right). Log in with the account *you* (Peter) use —
   NOT Jared's account. If you don't have an account yet, click **Sign Up**
   and make one (a free "Hobby" account is all you need).
3. **First, clean up the earlier attempt (if you have one).** If you already
   created a Render site from this and it's showing the wrong thing — a list
   of folders, or a different site, not the dugovic.com design — delete it:
   - Click on that service, open the **Settings** tab, and scroll to the very
     bottom of the page → **Delete**. Confirm when asked.
   - This only removes the Render service. It does **not** touch your files or
     your `dugovic.com` domain, so it's safe.
   - **If you haven't created one yet, skip this step.**
4. Click the big blue **New** button (top right). A small menu drops down.
5. In that menu, click **Static Site**.
6. A form appears with a step to **connect your repo**.
   - **Do NOT connect your GitHub account** — don't click a GitHub logo, don't
     sign in to GitHub, don't authorize or install any app.
   - Instead, look for the **Public Git Repository** option (a plain text box
     for a repo address). It may be a tab, toggle, or link below the
     repo list — the label is "Public Git Repository" or similar.
   - Paste this **exact address** into it:

   ```
   https://github.com/jared-the-automator/redesign-portfolio
   ```

   - That's the **whole repo** — that's correct. Do *not* add `/tree/...` or
     any other path after the repo name.
   - The branch should say **main** — leave it as is.
   - Click **Connect** (or **Continue**).
7. The rest of the form appears. Fill it in like this:

   | Field | Value | Why |
   |-------|-------|-----|
   | **Root Directory** | *(leave blank)* | The repo root is fine — the subfolder is handled by Publish Directory |
   | **Build Command** | *(leave blank)* | The HTML is already built — no build step needed |
   | **Publish Directory** | `./dugovic.com` | The static files live in the `dugovic.com` subfolder of the repo |

   > **This is the important step.** The key field is **Publish Directory =
   > `./dugovic.com`** (leave Root Directory blank). If it's blank or wrong,
   > Render will serve the whole repo — a list of folders — instead of the
   > dugovic site.

8. Click **Create Static Site** (or **Deploy**) at the bottom of the form.
9. You'll see a "deploying" screen with steps lighting up.
   - **Do nothing here.** It runs automatically. This takes 1–3 minutes.
   - When it's done, the item turns green and shows a URL like
     `dugovic.onrender.com`.
10. Open that `...onrender.com` URL in a new tab. **This is the moment of
    truth:** if the new dugovic site loads, Render is working. (The
    `dugovic.com` address still won't work yet — that's the next part.)

> **You're halfway done.** The website now exists on Render. The
> `dugovic.com` address just isn't pointing at it yet.

> ⚠️ **Important — this service will NOT update automatically.** Render
> only auto-deploys services that are connected through a Git provider
> (the "click the GitHub logo" flow we're intentionally avoiding). Because
> we're using a public repo URL, **every future update requires a manual
> deploy.** See "Updating the site later" at the bottom of this guide.

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
   - Check the list. `dugovic.com` and `www.dugovic.com` should be listed —
     they come in automatically if the service was created from the
     `render.yaml` Blueprint. If they're **not** listed, click
     **+ Add Custom Domain**, type `dugovic.com`, and save — Render will also
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
3. In the records list, exactly **two** rows control where the website goes:

   | Type | Name | What it points to now (the old Weebly site) |
   |------|------|---------------------------------------------|
   | `A` | `@` | `199.34.228.100` |
   | `CNAME` | `www` | `dugovic.com` |

   Everything else in the list — the two `MX` mail records, the
   `*.secureserver.net` CNAMEs, `_domainconnect`, `ftp`, `NS`, `SOA` — is for
   email or the domain itself. **Do not touch those.** There is no `AAAA`
   record to worry about.
4. **Edit** those two records in place (click the **pencil / Edit** icon on
   each row, change the value, then Save):

   | Type | Name/Host | New Data (Points to) |
   |------|-----------|----------------------|
   | `A` | `@` | `216.24.57.1` |
   | `CNAME` | `www` | `dugovic.onrender.com` ← use YOUR saved address from 2a.5 |

   Notes on typing these in:
   - For the `A` record, the name `@` means "the main domain." For the
     `CNAME`, keep the name `www`.
   - The `CNAME` value must be the `...onrender.com` address you saved in
     2a.5 — **not** `dugovic.com`.
   - **TTL**: leave it at the default (1 hour) — that's fine.
5. **Save** all changes.

> If GoDaddy shows a popup asking about "domain forwarding" or "website
> builder," **cancel it / say no** — we're not using forwarding, we're doing
> DNS records.

### 2c. Tell Render the DNS is set
1. Go back to the **Render → Settings → Custom Domains** page you kept open.
2. Next to `dugovic.com`, click **Verify** (you may need to refresh the page
   first).
3. Repeat for `www.dugovic.com` if it has its own Verify button.
4. This can take anywhere from a few minutes to ~30 minutes — occasionally
   longer (DNS changes "propagate" across the internet; GoDaddy notes up to
   48 h in the worst case). If it says "not found yet," wait 5 minutes and
   hit **Verify** again.
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
4. Go back to Weebly and **cancel / delete the old site** (or at minimum
   **disconnect `dugovic.com` from it**) so nobody pays for two things.
   - If the public URL **still shows the old Weebly site even though Part 2's
     DNS records are verified correct**, this step is *required*, not
     optional: the old site keeps serving the domain from Weebly's side, and
     the GoDaddy DNS records alone won't override that. Disconnect/cancel,
     wait ~5 minutes, retest.
   - If everything already looks right, you can instead leave Weebly running
     for a week; once you've confirmed the new site is solid, shut it off.
5. **Do NOT cancel the domain registration** — you only cancelled the
   Weebly *website*. Keep paying for `dugovic.com` where you always have.

---

## If something goes wrong

- **The `...onrender.com` URL from Part 1 works, but `dugovic.com` doesn't:**
  The DNS in Part 2 hasn't fully propagated or a record was typed wrong.
  Re-check the two records against the table in 2b.4. Confirm the `A` record
  value is exactly `216.24.57.1`.
- **`dugovic.com` loads the OLD Weebly site:** Two causes. (1) A DNS record
  still points to Weebly, or propagation is incomplete — re-check the two
  records in 2b.4 (the `A` value must be exactly `216.24.57.1`, the `www`
  CNAME must be exactly `dugovic.onrender.com`). (2) Both records are verified
  correct but the old site still loads — the old Weebly site is still
  connected to the domain on Weebly's side and its servers keep serving it;
  the DNS records alone can't override that. Go to Weebly and cancel /
  disconnect the old site (Part 3, Step 4), wait ~5 minutes, retest.
- **You get a 502 / "bad gateway" right after verifying:** Render is still
  wiring up routing. Wait a few minutes and reload.
- **It asks for money / cost isn't $0:** Stop and message Jared before you
  confirm.
- **You see a login screen or "not found" on the site itself** (not a DNS
  error): The site files didn't deploy. In Render, open the site → **Logs**,
  look for a red error, and send that screenshot to Jared.
- **Render keeps asking you to sign in to / connect your GitHub account:**
  You're on the "connect your account" option. Go back to Step 5 and use the
  **public repository URL** box instead — paste the exact URL from there. No
  GitHub login is needed.
- **The `...onrender.com` URL shows a list of folders or a different site**
  (not the dugovic site): The subfolder wasn't applied. Open the service →
  **Settings** → **Build** and check that **Publish Directory** is
  `./dugovic.com` (Root Directory stays blank). Save, then trigger a manual
  deploy (see "Updating the site later").
- **I pushed a new commit but the site didn't update:** Expected — public-repo
  services don't auto-deploy. Go to the service → **Manual Deploy** →
  **Deploy latest commit**.

## What NOT to do
- Don't "transfer the domain into Render" unless we specifically ask — we're
  intentionally keeping the registration at your current registrar.
- Don't type a `CNAME` for the `@`/root record (only `www` gets a CNAME).
- Don't delete the `AAAA` record until after the new `A` record is in place,
  or the site will be unreachable for a moment.
- Don't delete the domain registration — only the Weebly *website* gets
  turned off; keep paying for `dugovic.com` at your registrar.
- If the public URL still shows the old site after the Part 2 DNS records are
  confirmed correct, don't keep waiting on propagation — disconnect the old
  site on Weebly's side (Step 4); it's still serving the domain there.

---

## Updating the site later

Because this service uses a **public repo URL** (not a connected GitHub
account), Render does **not** automatically rebuild when new commits are
pushed. To publish an update:

1. After Jared commits + pushes the change to the repo, go to the
   **dugovic** service in the Render dashboard.
2. Click **Manual Deploy** → **Deploy latest commit**.
3. Wait for the build to finish, then reload the site.

(If you'd rather have automatic deploys on every push, connect the
`jared-the-automator` GitHub account to Render under **Account Settings →
Git Deployment Credentials** and link the repo — then Render rebuilds on each
push.)

---
*Technical reference version: see `DEPLOY.md` (same folder) if you want the
short version without the hand-holding.*
