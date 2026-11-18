# Deploying dugovic.com to Render

This repo holds the redesign of **dugovic.com**. The site is a static
site: the published files live in `dugovic.com/` (HTML + `assets/`).
`dugovic.com/generate_site.py` regenerates the HTML from `cats.json` and
`comic_order.json` — run `python3 dugovic.com/generate_site.py` whenever
the image catalog or copy changes, then commit the resulting HTML.

`render.yaml` (this repo root) is a **Render Blueprint** that provisions the
whole site as one static service. You can deploy from the Blueprint or set
it up by hand — both are below.

## Option A — one-click from the Blueprint (recommended)

1. Go to https://dashboard.render.com → **New → Blueprint**.
2. Connect this repo (`jared-the-automator/redesign-portfolio`, branch `main`).
   Render finds `render.yaml` and provisions a static site named `dugovic`
   with `dugovic.com` and `www.dugovic.com` already attached.
3. Let the first deploy finish (a `*.onrender.com` URL appears).
4. Point DNS (next section), then hit **Verify** on each custom domain in the
   Render dashboard. Done.

## Option B — manual static-site setup

1. **New → Static Site** → connect this repo, branch `main`.
2. Root directory: `dugovic.com`
3. Build command: *(leave empty)* — the HTML is pre-generated and committed.
   (If you prefer building on Render: `python3 generate_site.py`.)
4. Publish directory: `dugovic.com`
5. **Settings → Custom Domains** → add `dugovic.com`. Render auto-adds
   `www.dugovic.com` and sets up the redirect.

## Pointing the domain at Render (from Weebly / GoDaddy)

The domain is currently on Weebly. You don't have to move the *registration*
— just repoint its DNS. Do this in whatever panel manages `dugovic.com`
(GoDaddy, Weebly's domain manager, etc.):

Remove existing A / AAAA / CNAME records that point to Weebly, then add:

| Type  | Host / Name | Value | Notes |
|-------|-------------|-------|-------|
| `A`   | `@`         | `216.24.57.1` | apex — Render's load-balancer IP |
| `CNAME`| `www`      | `<your-site>.onrender.com` | exact subdomain shown in the Render dashboard |

- Set TTL to **1 minute** to speed up verification.
- **Delete any `AAAA` record** — Render is IPv4-only and stale IPv6 records
  cause failures.
- If you use Cloudflare instead: use a **CNAME** for `@` (flattening) and set
  proxy to **DNS only** (grey cloud) first, so Render can verify + issue TLS.

## Verify

1. Back in Render → **Settings → Custom Domains** → **Verify** for each domain.
2. Render auto-issues + renews TLS (Let's Encrypt / Google Trust Services).
3. When the status shows **Verified**, visit `https://dugovic.com`.
4. Optionally disable the default `*.onrender.com` subdomain
   (Settings → Custom Domains) so the site is only reachable at your domain.

## Ongoing

Every push to `main` redeploys automatically. To change copy or the image
catalog: edit `generate_site.py` / `cats.json`, regenerate, commit, push —
Render picks it up.
