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
| `draft-v0.2.md` | Prose source of record, citation register, and pre-send checklist. |

## Open items (mirrors the checklist in `draft-v0.2.md`)

1. Transcribe the discharge-curve values from the FPV-school slide into
   `DISCHARGE_DATA` in `figures.js` — Figure 2 renders its frame and verified
   anchors until then.
2. Recover t.me/ URLs for the RU-language source register.
3. Resolve the Seto et al. DRDC accession number (footnote 1).
4. Image pass rules and the read-aloud pass — see the checklist in the draft.

Figure numbering note: figures are numbered in reading order of the brief —
1 = two-corpora timeline (§3a), 2 = discharge scaffold (§3b), 3 = landing-reserve
spread (§3b) — which differs from the original mockup's order (reserve was 2,
discharge was 3).
