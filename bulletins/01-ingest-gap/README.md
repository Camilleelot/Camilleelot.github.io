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

## Release gates (v1.0-rc → v1.0) — all Camille's

1. Pixel-verify the five `DISCHARGE_DATA` values in `figures.js` against the
   deck slide (and the rated-capacity baseline), then remove the transcription
   caveats from both pages.
2. Confirm in the Telegram app that Ratnik2nd/6222 and getyourdrone/468 are
   2026 posts; remove the register caveats.
3. Resolve or accept the «Соколы Хоруса»-vs-deck-school identity flag.
4. Read-aloud pass — substantial passages are assistant-drafted and need to
   come out in Camille's voice.

Then: bump header/footer to v1.0, rename the draft file, update links here
and in `index.html`. Everything else is closed — details in `changelog.md`.

Figure numbering note: figures are numbered in reading order of the brief —
1 = two-corpora timeline (§3a), 2 = discharge scaffold (§3b), 3 = landing-reserve
spread (§3b) — which differs from the original mockup's order (reserve was 2,
discharge was 3).
