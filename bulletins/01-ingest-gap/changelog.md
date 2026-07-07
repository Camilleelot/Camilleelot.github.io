# Changelog — Bulletin 01: The Ingest Gap

Working history of the brief, arXiv-style. The prose source of record is the
current `draft-*.md`; this file carries what changed between versions.

## v1.0-rc — July 6, 2026

Second pass (editor's notes):

- Em dashes purged throughout; prose de-cringed; first person adopted where
  the author speaks ("translations are mine," "my reading of the deck's
  curves").
- §1/§4: explicit civil-vs-military framing added. The CARs bind civil
  operators; the CAF flies under DND airworthiness and flying orders; the
  objection sharpens the gap because the military layer that would supersede
  the civil rule is exactly what the published record lacks.
- Figure 1 now states its argument in-figure: per-track headers with bold
  item counts and the question each track answers.
- Figure captions moved to the right margin beside their figures (marginnote
  markup; the old markup put the caption after the content, which floated it
  below). Figure 1's caption rides the margin beside the following paragraph.
- Figure 2 reframed as an approximate reproduction of the deck's slide by
  design; pixel-verification gate dropped.
- In-app year-check gate dropped; the two 2026 dates stand on the Telegram
  current-year embed inference.
- Patch-board insignia identified in the caption, read directly from the
  patches, with the photo dated late 2023; §3c names the spread of
  formations in prose.
- On-page register simplified to Source and Type, links removed, statuses
  removed; screenshot-archive rows say so. Verification detail stays in the
  draft's working register.
- Canadian baseline documents linked in the draft for the annotation pass
  (CAR 901.35, TP 15263E PDF, TR 2013-142, NRC Phase 2 DOI; all verified
  live).
- Release gates reduced to two: the deck-school confirmation and the
  read-aloud pass.

First pass:

- MINDS recommendation (§5) aligned to the named 2025–26 Defence Policy
  Challenges: "Canada Strong — in the Arctic, the North, and North America"
  and the Ukraine-lessons research question under the strategic-competition
  challenge.
- Seto et al. accession number accepted as unresolved for 1.0 — cited by
  author/title/year per footnote 1. DRDC publications portal was unreachable
  (HTTP 503); candidate record SYSNUM 534115 noted in the register for one
  retry.
- Working notes pruned to the four release gates (pixel-verify Figure 2;
  in-app year check on two posts; the school-identity flag; read-aloud pass).
- Figures redesigned: theme-aware light/dark palettes selected per
  prefers-color-scheme and re-rendered on change, colors validated against
  both site surfaces (light #2b6fa8/#8a5a00 on #fffff8, dark #4f97cc/#c98500
  on #151515); headline counts on the Figure 1 tracks; drop lines, leader
  lines, and stage bands; area wash and cold-start-risk zone on Figure 2;
  Figure 3 re-drawn as an honest range strip (operator claim is itself
  20–30%); tooltips on all marks. Fixed: figures were illegible in the
  site's dark mode (hardcoded near-black ink).
- Citation register: RU-source URL recovery closed — the four verified links
  are the complete recoverable set; remaining items marked as cited from the
  author's screenshot archive.

## v0.4 — July 6, 2026

- The 2023 FPV-school deck reviewed from slides (7 in archive). Two
  corrections: (1) −20°C useful capacity is ≈54% of rated read to the 3.0 V
  cutoff, not ~30% — the deck's "30%" is its separate "discharges at least
  30% faster" text claim; the chart is a datasheet-style voltage-vs-capacity
  family, flagged as such. (2) Winter battery load-out is internally
  divergent within the deck (10–12 on the problem slide vs. 10–15 on the kit
  list) and is reported as a spread, strengthening the
  doctrine-not-consolidated finding.
- Figure 2 curves transcribed (author's eyeball reading, flagged pending
  pixel verification).
- Added: 22-item winter kit list (§3a); discreditation-statute worked
  example (§3d); bench and patch-board photographs (§3c; EXIF verified
  clean, no identifiable persons, per §3d rules).

## v0.3 — July 5, 2026

- Four t.me URLs recovered and verified via Telegram embed pages:
  dva_majors/7931 (Jan 17, 2023), dronnitsa/284 (Aug 26, 2023),
  Ratnik2nd/6222 (Jan 24, 2026*), getyourdrone/468 (Apr 13, 2026*).
  *Current-year inference; in-app check is release gate 2.
- Added: frontline northern-latitudes post to §1 (the "Greenland" post);
  battery-behaviour mechanism and unit-level battery logistics to §3b;
  full-cycle pedagogy and the patch-board feedback loop to §3c; the school's
  silicone workflow to §3a.

## v0.2 — July 2, 2026

- Sections 1–5 drafted in full; Canadian-side citations verified
  (TR 2013-142, NRC icing series DOI, TP 15263E rev. 03/2025, MINDS TEG
  parameters). Initial figure mockups.
