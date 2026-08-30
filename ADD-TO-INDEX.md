# Adding Lapse Watch to the site

## ⚠ Read this before you commit anything

`C:\Users\Camille\Documents\GitHub\Camilleelot.github.io` is **146 commits behind origin/main**
and has uncommitted local changes (`index.html` modified, plus untracked `test.txt.html`,
`transit-voting.html`, `viz/`, `.claude/`). That clone predates `bulletins/`, `fleet-management/`,
`colors.css`, the self-hosted fonts, and the whole `papers/` restructure.

**If you commit and push from that working tree you will clobber the live site.** Fix the clone
first — either move it aside and re-clone, or stash what you want and hard-reset onto origin:

```bash
cd ~/Documents/GitHub/Camilleelot.github.io && git stash -u && git reset --hard origin/main
```

I built this page against a clean extract of `origin/main`, not against that stale tree, and I
haven't touched your repo.

## Then

1. Copy the whole `foundry-lapse-watch/` folder into the repo root (sibling of `fleet-management/`).
2. Paste the card below into `index.html`, right after the **Bulletin 01: The Ingest Gap** article.
   Renumber `§ 07` if the count has moved.

```html
      <!-- Lapse Watch -->
      <article class="also-item">
        <div>
          <div class="num">§ 07 · Deployment · Palantir Foundry · 2026</div>
          <h4>Lapse Watch <em>for grandfathered approvals</em>.</h4>
          <p class="s">A work queue for 1,365 rezoning approvals quietly counting down to expiry.</p>
          <p class="d i-line">
            Calgary repealed blanket rezoning on 4 August 2026. Approvals granted before the repeal keep
            their density only until a commencement deadline passes &mdash; then they lapse onto land that
            has reverted, and the density cannot be re-earned. <u>I taught myself Palantir Foundry and
            built the whole deployment solo</u>: incremental Socrata ingestion with watermarking and
            transactional rollback, a four-object ontology, and a ranked operator queue with writeback.
            Screen recordings of the running app, because the stack itself is access-gated. No user has
            ever operated it but me.
          </p>
          <p class="links">
            <a href="foundry-lapse-watch/">Project &amp; recordings &rarr;</a>
          </p>
        </div>
        <div class="spark-box">
          <div class="stat-n">1,365</div>
          <div class="stat-l">Approvals still saveable<br/>(1,569 units at risk)</div>
          <svg viewBox="0 0 140 54" width="140" height="54" aria-label="Ingestion to operator queue diagram">
            <g font-family="JetBrains Mono, monospace" font-size="7" fill="var(--ink-2)" letter-spacing="0.06em">
              <rect x="2"   y="20" width="36" height="16" fill="none" stroke="var(--ink-3)" stroke-width="0.8"/>
              <text x="6"   y="31">INGEST</text>
              <rect x="52"  y="20" width="36" height="16" fill="none" stroke="var(--ink-3)" stroke-width="0.8"/>
              <text x="53"  y="31">ONTOL.</text>
              <rect x="102" y="20" width="36" height="16" fill="none" stroke="var(--accent)" stroke-width="1.2"/>
              <text x="106" y="31" fill="var(--accent)">QUEUE</text>
            </g>
            <g stroke="var(--ink-3)" stroke-width="0.8">
              <line x1="38" y1="28" x2="52" y2="28"/>
              <line x1="88" y1="28" x2="102" y2="28"/>
            </g>
            <path d="M120 40 v6 h-100 v-6" fill="none" stroke="var(--accent)" stroke-width="0.8" stroke-dasharray="2 2"/>
            <text x="2" y="10" font-family="JetBrains Mono, monospace" font-size="6.5" fill="var(--ink-3)" letter-spacing="0.1em">DAILY &rarr; WRITEBACK LOOP</text>
          </svg>
        </div>
      </article>
```

3. Add to `sitemap.xml` alongside the other pages.

## What's in the folder

| file | |
|---|---|
| `index.html` | The case-study page. Uses `../tufte.css`, `../latex.css`, `../colors.css`, so it only renders correctly once it's in the repo root. |
| `lapse-watch-writeback.gif` | 880px, 1.06 MB — row select → Log Outreach → writeback confirmed |
| `ontology-development-permit.gif` | 880px, 0.40 MB — Ontology Manager → Development Permit → 30 properties |

Larger cuts (1100px and full-res 1568px) are loose in `Downloads/` if you want them.

## Claim discipline

The page carries a **"What this does not have"** block, in your own framing: no user, no City
engagement, no adoption, no approval saved. The twenty logged runs are described as evidence the
pipeline works, explicitly not evidence anything was rescued. Don't quietly delete that — it's the
thing that makes the rest of the page credible, and it matches what your CVs and WaaS profile
already say.
