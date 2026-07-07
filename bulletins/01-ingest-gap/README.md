# Bulletin 01 — The Ingest Gap (unlisted) · v1.0-rc

Working project for the Arctic doctrine brief. This directory is deliberately
**not linked from the site index or `sitemap.xml`**, and both HTML pages carry
`<meta name="robots" content="noindex, nofollow">`. It is reachable only by
direct URL:

    https://camilleelot.github.io/bulletins/01-ingest-gap/

Share that link directly with the people who should read it.

## Files

| File | Role |
|---|---|
| `index.html` | The rendered brief (Tufte layout, figures and photos inline). This is the page to send. |
| `figures.js` | All three d3 figures — theme-aware (light/dark), shared by both pages; edit data here once. |
| `figures.html` | Standalone figure workbench for iterating on the visuals. |
| `draft-v1.0-rc.md` | Prose source of record, citation register, and the release checklist. |
| `changelog.md` | Version history, v0.2 → v1.0-rc. |

Photographs live in the site-level `/img/` (Cropped Bench.jpg, Patches
Board.jpg — EXIF-clean, no identifiable persons, per the brief's §3d rules).
`d3.v7.min.js` is vendored at the site root.

## Release gates (v1.0-rc → v1.0) — both Camille's

1. Confirm the 2023 curriculum deck belongs to «Соколы Хоруса» (the patch
   board already carries the school's own operator patch, so the photos are
   anchored; only the deck's attribution is open).
2. Read-aloud pass in Camille's voice.

Decisions on record (July 6, 2026): Figure 2 is an approximate reproduction
of the deck's slide by design, no pixel verification pass; the two 2026 post
dates stand on the Telegram current-year embed inference, no in-app check;
no em dashes anywhere; first person allowed; the on-page register is
simplified to Source and Type (verification detail stays in the draft);
patch-board insignia are identified in the caption, read directly from the
patches; §1/§4 now state explicitly that the CARs are civil rules and why
they still set the Canadian baseline.

Then: bump header/footer to v1.0, rename the draft file, update links here
and in `index.html`. Details in `changelog.md`.

Figure numbering note: figures are numbered in reading order of the brief —
1 = two-corpora timeline (§3a), 2 = discharge scaffold (§3b), 3 = landing-reserve
spread (§3b) — which differs from the original mockup's order (reserve was 2,
discharge was 3).
