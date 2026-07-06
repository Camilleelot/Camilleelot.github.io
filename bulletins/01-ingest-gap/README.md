# Bulletin 01 — The Ingest Gap (unlisted)

Working project for the Arctic doctrine brief. This directory is deliberately
**not linked from the site index or `sitemap.xml`**, and both HTML pages carry
`<meta name="robots" content="noindex, nofollow">`. It is reachable only by
direct URL:

    https://camilleelot.github.io/bulletins/01-ingest-gap/

Share that link directly with the people who should read it.

## Files

| File | Role |
|---|---|
| `index.html` | The rendered brief (Tufte layout, figures inline). This is the page to send. |
| `figures.js` | All three d3 figures. Shared by both pages — edit data here once. |
| `figures.html` | Standalone figure workbench for iterating on the visuals. |
| `draft-v0.3.md` | Prose source of record, citation register, and pre-send checklist. |

## Open items (mirrors the checklist in `draft-v0.3.md`)

1. Transcribe the discharge-curve values from the FPV-school slide into
   `DISCHARGE_DATA` in `figures.js` — Figure 2 renders its frame and verified
   anchors until then.
2. Recover remaining t.me/ URLs for the RU-language source register
   (done July 5, 2026: dva_majors/7931, dronnitsa/284, Ratnik2nd/6222,
   getyourdrone/468 — verified via t.me embed pages; still missing: the 2023
   school deck, «Соколы Хоруса» posts, mil_hub, FPV_выZOV, Техник БПЛА,
   notes_veterans).
3. Resolve the Seto et al. DRDC accession number (footnote 1).
4. Image pass rules and the read-aloud pass — see the checklist in the draft.
   Source photos (classroom, Ratnik2nd, patch board) are deliberately NOT in
   this repo: per the brief's own §3d rules they are described in text, not
   reproduced.

Figure numbering note: figures are numbered in reading order of the brief —
1 = two-corpora timeline (§3a), 2 = discharge scaffold (§3b), 3 = landing-reserve
spread (§3b) — which differs from the original mockup's order (reserve was 2,
discharge was 3).
