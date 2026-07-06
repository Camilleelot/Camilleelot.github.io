/* Figures for "The Ingest Gap" — bulletin 01.
   Each figure renders only if its container div exists, so this one file
   drives both index.html (the brief) and figures.html (the workbench).
   Requires d3 v7 to be loaded first.

   Theme-aware: colors are chosen per prefers-color-scheme (the site's
   tufte.css surfaces are #fffff8 light / #151515 dark) and the figures
   re-render when the scheme changes. Marks carry the data; text stays in
   ink/secondary/muted tokens. One accent hue: the frontline corpus. */

function pal() {
  const dark = window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;
  return dark ? {
    surface: "#151515",
    ink: "#dddddd",       // primary text/marks (matches tufte dark body)
    secondary: "#a8a69e",
    muted: "#8a8880",
    axis: "#6a6a6a",
    grid: "#33322f",
    accent: "#4f97cc",    // frontline corpus, stepped for the dark surface (validated)
    accentText: "#9dc2da",
    warn: "#c98500"       // thresholds, stepped for the dark surface (validated)
  } : {
    surface: "#fffff8",
    ink: "#111111",
    secondary: "#444444",
    muted: "#777777",
    axis: "#999999",
    grid: "#d8d5c9",
    accent: "#2b6fa8",    // validated against #fffff8 (chroma floor, CVD, contrast)
    accentText: "#2c536b",
    warn: "#8a5a00"
  };
}

/* ---------------------------------------------------------------
   Data. Dates marked "verified" are pinned by t.me embed pages
   (July 5, 2026); the rest are approximate from the author's
   screenshot archive (no public URLs survive — register, July 6).
---------------------------------------------------------------- */
const CAN = [
  {d: 2012.6, label: "CFJAE12, Gascoyne Inlet"},
  {d: 2013.5, label: "DRDC TR 2013-142"},
  {d: 2019.4, label: "CARs Part IX · TP 15263"},
  {d: 2020.3, label: "NRC icing series, Ph. 1–4"},
  {d: 2025.2, label: "SOR/2025-70 · TP 15263E rev."}
];
const RU = [ // {d, s: stage 1|2|3, label (optional, only majors get text)}
  {d: 2022.85, s: 1}, {d: 2022.95, s: 1, label: "improvisation: salo, bottles, hand-warmers"},
  {d: 2023.05, s: 1}, // verified: dva_majors/7931 trench candle, Jan 17 2023
  {d: 2023.1, s: 1}, {d: 2023.2, s: 1},
  {d: 2023.45, s: 2, label: "FPV school winter deck · 22-item kit"},
  {d: 2023.6, s: 2},
  {d: 2023.65, s: 2}, // verified: dronnitsa/284 battery org checklist, Aug 26 2023
  {d: 2023.75, s: 2}, {d: 2023.9, s: 2, label: "AERO LIGHT · АНТИЛЕД · B-7000"},
  {d: 2023.95, s: 1}, {d: 2024.0, s: 1}, {d: 2024.1, s: 2}, {d: 2024.2, s: 2},
  {d: 2024.5, s: 3}, {d: 2024.8, s: 2}, {d: 2024.9, s: 2},
  {d: 2025.0, s: 2}, {d: 2025.17, s: 3, label: "Geran-2 «Зима» kit in production"},
  {d: 2025.4, s: 3}, {d: 2025.85, s: 2}, {d: 2025.95, s: 2},
  {d: 2026.0, s: 2, label: "mil_hub battery protocol · TO-1(2) framing"},
  {d: 2026.05, s: 2},
  {d: 2026.07, s: 1}, // verified: Ratnik2nd/6222 northern-latitudes post, Jan 24 2026
  {d: 2026.1, s: 2}, {d: 2026.15, s: 2},
  {d: 2026.28, s: 2}  // verified: getyourdrone/468 battery behaviour, Apr 13 2026
];
const STAGES = [
  {a: 2022.8, b: 2023.6, t: "1 · improvisation"},
  {a: 2023.3, b: 2025.1, t: "2 · aftermarket"},
  {a: 2024.4, b: 2026.4, t: "3 · productization"}
];

const DISCHARGE_DATA = [
  // Author's eyeball transcription (July 6, 2026) of the deck's
  // voltage-vs-capacity curve family, read at the 3.0 V cutoff and
  // normalized to the +45°C curve (~2000 mAh ≈ rated).
  // VERIFY against the slide pixels before publication.
  { name: "capacity to 3.0 V cutoff, % of rated — author's reading",
    pts: [{t: -20, c: 54}, {t: -10, c: 82}, {t: 0, c: 95}, {t: 23, c: 97}, {t: 45, c: 100}] }
];
const VERIFIED_ANCHORS = [
  {t: -20, c: 54, label: "≈54% of rated at −20°C (deck curves, 2023)"}
];

/* ---------------------------------------------------------------
   FIGURE 1 — The Ingest Gap timeline
---------------------------------------------------------------- */
function fig1(P) {
  const el = document.getElementById("fig-gap");
  if (!el) return;
  const W = 860, H = 340, m = {t: 34, r: 30, b: 40, l: 30};
  const svg = d3.select(el).append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`).attr("width", "100%");
  const x = d3.scaleLinear().domain([2011.8, 2026.7]).range([m.l, W - m.r]);
  const yCAN = 96, yRU = 212, axisY = H - m.b;

  // time axis — hairline, recessive
  const ax = d3.axisBottom(x).tickValues(d3.range(2012, 2027, 2))
    .tickFormat(d3.format("d")).tickSize(4);
  svg.append("g").attr("transform", `translate(0,${axisY})`).call(ax)
    .call(g => { g.select(".domain").attr("stroke", P.axis);
                 g.selectAll("text").attr("fill", P.muted).style("font-size", "11px");
                 g.selectAll("line").attr("stroke", P.axis); });

  // Feb 2022 event line (dashed = a threshold, not a gridline)
  svg.append("line").attr("x1", x(2022.12)).attr("x2", x(2022.12))
    .attr("y1", m.t).attr("y2", axisY).attr("stroke", P.muted)
    .attr("stroke-dasharray", "2,3");
  svg.append("text").attr("x", x(2022.12)).attr("y", m.t - 10)
    .attr("text-anchor", "middle").attr("fill", P.secondary).style("font-size", "10.5px")
    .style("font-style", "italic").text("Feb 2022 — the FPV revolution begins");

  // track labels, with the headline counts — the argument as a number
  svg.append("text").attr("x", m.l).attr("y", yCAN - 38).attr("fill", P.ink)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text(`canadian published corpus — ${CAN.length} items in 14 years`);
  svg.append("text").attr("x", m.l).attr("y", yRU + 4).attr("fill", P.accentText)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text(`russian / ukrainian frontline corpus — ${RU.length} items in 4 winters`);

  // Canadian items: open circles with hairline drops to the axis,
  // so the emptiness between them is legible as time
  svg.selectAll(".cand").data(CAN).join("line")
    .attr("x1", d => x(d.d)).attr("x2", d => x(d.d))
    .attr("y1", yCAN + 5).attr("y2", axisY)
    .attr("stroke", P.grid).attr("stroke-width", 1);
  svg.selectAll(".can").data(CAN).join("circle")
    .attr("cx", d => x(d.d)).attr("cy", yCAN).attr("r", 5)
    .attr("fill", P.surface).attr("stroke", P.ink).attr("stroke-width", 1.6)
    .each(function(d){ d3.select(this).append("title")
      .text(`${d.label} — ${Math.floor(d.d)}`); });
  svg.selectAll(".canl").data(CAN).join("text")
    .attr("x", d => x(d.d)).attr("y", (d, i) => yCAN + (i % 2 ? 24 : -16))
    .attr("text-anchor", "middle").attr("fill", P.secondary).style("font-size", "10.5px")
    .text(d => d.label);

  // frontline rug — density is the argument
  svg.selectAll(".ru").data(RU).join("line")
    .attr("x1", d => x(d.d)).attr("x2", d => x(d.d))
    .attr("y1", yRU - 11).attr("y2", yRU + 11)
    .attr("stroke", P.accent).attr("stroke-width", 2.2).attr("opacity", .95)
    .each(function(d){ d3.select(this).append("title")
      .text(d.label ? d.label : `frontline corpus item, ~${Math.floor(d.d)} (stage ${d.s})`); });

  // labeled majors — one row each, tied to their ticks by hairline leaders
  const majors = RU.filter(d => d.label);
  const rowY = i => yRU - 24 - i * 13;
  svg.selectAll(".rull").data(majors).join("line")
    .attr("x1", d => x(d.d)).attr("x2", d => x(d.d))
    .attr("y1", (d, i) => rowY(i) + 3).attr("y2", yRU - 13)
    .attr("stroke", P.grid).attr("stroke-width", 1);
  svg.selectAll(".rul").data(majors).join("text")
    .attr("x", d => x(d.d))
    .attr("y", (d, i) => rowY(i))
    .attr("text-anchor", d => d.d > 2025.6 ? "end" : "middle")
    .attr("fill", P.secondary).style("font-size", "10px")
    .text(d => d.label);

  // stage bands — washes with weight, not skinny brackets
  STAGES.forEach((s, i) => {
    const y = yRU + 18 + i * 14;
    svg.append("rect").attr("x", x(s.a)).attr("y", y)
      .attr("width", x(s.b) - x(s.a)).attr("height", 11).attr("rx", 2)
      .attr("fill", P.accent).attr("opacity", .12);
    svg.append("text").attr("x", x(s.a) - 6).attr("y", y + 9)
      .attr("text-anchor", "end").attr("fill", P.accentText)
      .style("font-size", "9.5px").style("font-style", "italic").text(s.t);
  });
}

/* ---------------------------------------------------------------
   FIGURE 2 — useful capacity vs. ambient temperature
---------------------------------------------------------------- */
function fig2(P) {
  const el = document.getElementById("fig-discharge");
  if (!el) return;
  const W = 620, H = 310, m = {t: 30, r: 30, b: 44, l: 52};
  const svg = d3.select(el).append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`).attr("width", "100%").style("max-width", "620px");
  const x = d3.scaleLinear().domain([-25, 47]).range([m.l, W - m.r]);
  const y = d3.scaleLinear().domain([0, 100]).range([H - m.b, m.t]);

  // recessive grid: hairlines at 50 and 100
  [50, 100].forEach(v => {
    svg.append("line").attr("x1", m.l).attr("x2", W - m.r)
      .attr("y1", y(v)).attr("y2", y(v)).attr("stroke", P.grid).attr("stroke-width", 1);
  });

  const axX = d3.axisBottom(x).tickValues([-20, -15, -10, 0, 23, 45])
    .tickFormat(d => d + "°").tickSize(4);
  const axY = d3.axisLeft(y).tickValues([0, 50, 100])
    .tickFormat(d => d + "%").tickSize(4);
  svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(axX)
    .call(g => { g.select(".domain").attr("stroke", P.axis);
                 g.selectAll("text").attr("fill", P.muted).style("font-size", "11px");
                 g.selectAll("line").attr("stroke", P.axis); });
  svg.append("g").attr("transform", `translate(${m.l},0)`).call(axY)
    .call(g => { g.select(".domain").remove();
                 g.selectAll("text").attr("fill", P.muted).style("font-size", "11px");
                 g.selectAll("line").attr("stroke", P.axis); });

  // cold-start risk zone left of −15°C, then the threshold itself
  svg.append("rect").attr("x", m.l).attr("y", y(100))
    .attr("width", x(-15) - m.l).attr("height", y(0) - y(100))
    .attr("fill", P.warn).attr("opacity", .06);
  svg.append("line").attr("x1", x(-15)).attr("x2", x(-15))
    .attr("y1", y(100)).attr("y2", y(0)).attr("stroke", P.warn)
    .attr("stroke-dasharray", "2,3");
  svg.append("text").attr("x", x(-15) + 8).attr("y", y(5))
    .attr("text-anchor", "start").attr("fill", P.warn).style("font-size", "10px")
    .style("font-style", "italic").text("BLDC cold-start threshold −15°C");

  if (DISCHARGE_DATA.length === 0) {
    svg.append("text").attr("x", (m.l + W - m.r) / 2).attr("y", y(72))
      .attr("text-anchor", "middle").attr("fill", P.muted)
      .style("font-size", "12px").style("font-style", "italic")
      .text("curves render when DISCHARGE_DATA is transcribed from the source slide");
  } else {
    const line = d3.line().x(p => x(p.t)).y(p => y(p.c)).curve(d3.curveMonotoneX);
    const area = d3.area().x(p => x(p.t)).y0(y(0)).y1(p => y(p.c)).curve(d3.curveMonotoneX);
    DISCHARGE_DATA.forEach(s => {
      // the wash is what the cold leaves you; the void above-left is what it takes
      svg.append("path").attr("d", area(s.pts)).attr("fill", P.accent).attr("opacity", .10);
      svg.append("path").attr("d", line(s.pts)).attr("fill", "none")
        .attr("stroke", P.accent).attr("stroke-width", 2)
        .attr("stroke-linejoin", "round").attr("stroke-linecap", "round");
      svg.selectAll(null).data(s.pts).join("circle")
        .attr("cx", p => x(p.t)).attr("cy", p => y(p.c)).attr("r", 4)
        .attr("fill", P.accent).attr("stroke", P.surface).attr("stroke-width", 2)
        .each(function(p){ d3.select(this).append("title")
          .text(`${p.t}°C → ≈${p.c}% of rated`); });
      const last = s.pts[s.pts.length - 1];
      svg.append("text").attr("x", x(last.t)).attr("y", y(last.c) + 18)
        .attr("text-anchor", "end")
        .attr("fill", P.secondary).style("font-size", "10px").text(s.name);
    });
  }

  // the −20°C anchor: emphasized point with Tufte drop-lines to both axes
  VERIFIED_ANCHORS.forEach(a => {
    svg.append("line").attr("x1", m.l).attr("x2", x(a.t))
      .attr("y1", y(a.c)).attr("y2", y(a.c)).attr("stroke", P.grid).attr("stroke-width", 1);
    svg.append("line").attr("x1", x(a.t)).attr("x2", x(a.t))
      .attr("y1", y(a.c)).attr("y2", y(0)).attr("stroke", P.grid).attr("stroke-width", 1);
    svg.append("circle").attr("cx", x(a.t)).attr("cy", y(a.c)).attr("r", 5)
      .attr("fill", P.accent).attr("stroke", P.surface).attr("stroke-width", 2);
    svg.append("text").attr("x", x(a.t) + 10).attr("y", y(a.c) - 8)
      .attr("fill", P.secondary).style("font-size", "10.5px").text(a.label);
  });

  svg.append("text").attr("x", m.l).attr("y", m.t - 12).attr("fill", P.ink)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text("useful capacity vs. ambient temperature");
}

/* ---------------------------------------------------------------
   FIGURE 3 — landing-reserve spread (range strip, honest about the
   operator claim being itself a 20–30% range)
---------------------------------------------------------------- */
function fig3(P) {
  const el = document.getElementById("fig-reserve");
  if (!el) return;
  const W = 620, H = 190, m = {t: 26, r: 40, b: 34, l: 40};
  const svg = d3.select(el).append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`).attr("width", "100%").style("max-width", "620px");
  const x = d3.scaleLinear().domain([0, 50]).range([m.l, W - m.r]);
  const y = 100, axisY = H - m.b;

  const ax = d3.axisBottom(x).tickValues([0, 10, 20, 30, 40, 50])
    .tickFormat(d => d + "%").tickSize(4);
  svg.append("g").attr("transform", `translate(0,${axisY})`).call(ax)
    .call(g => { g.select(".domain").attr("stroke", P.axis);
                 g.selectAll("text").attr("fill", P.muted).style("font-size", "11px");
                 g.selectAll("line").attr("stroke", P.axis); });

  // the full winter spread, 20–40, as a soft band
  svg.append("rect").attr("x", x(20)).attr("y", y - 7)
    .attr("width", x(40) - x(20)).attr("height", 14).attr("rx", 7)
    .attr("fill", P.accent).attr("opacity", .12)
    .append("title").text("winter landing-reserve spread across sources: 20–40%");

  // operator claim is itself a range: solid 20–30 segment
  svg.append("rect").attr("x", x(20)).attr("y", y - 2.5)
    .attr("width", x(30) - x(20)).attr("height", 5).attr("rx", 2.5)
    .attr("fill", P.accent)
    .append("title").text("operator channel, Jan 2026: land at 20–30% reserve");
  // deck claim: a single point at 40
  svg.append("circle").attr("cx", x(40)).attr("cy", y).attr("r", 5)
    .attr("fill", P.accent).attr("stroke", P.surface).attr("stroke-width", 2)
    .append("title").text("FPV school training deck, 2023: land at 40% reserve");

  // labels on two rows, tied down by hairline leaders
  svg.append("text").attr("x", x(25)).attr("y", y - 34)
    .attr("text-anchor", "middle").attr("fill", P.secondary)
    .style("font-size", "10.5px").text("operator channel, Jan 2026: 20–30%");
  svg.append("line").attr("x1", x(25)).attr("x2", x(25))
    .attr("y1", y - 30).attr("y2", y - 10).attr("stroke", P.grid).attr("stroke-width", 1);
  svg.append("text").attr("x", x(40)).attr("y", y - 18)
    .attr("text-anchor", "middle").attr("fill", P.secondary)
    .style("font-size", "10.5px").text("training deck, 2023: 40%");
  svg.append("line").attr("x1", x(40)).attr("x2", x(40))
    .attr("y1", y - 14).attr("y2", y - 7).attr("stroke", P.grid).attr("stroke-width", 1);

  // summer comparator on its own quiet row
  svg.append("circle").attr("cx", x(20)).attr("cy", y + 28).attr("r", 4)
    .attr("fill", P.surface).attr("stroke", P.ink).attr("stroke-width", 1.4)
    .append("title").text("typical summer landing reserve: 20%");
  svg.append("text").attr("x", x(20) + 10).attr("y", y + 32).attr("fill", P.secondary)
    .style("font-size", "10.5px").text("typical summer reserve: 20%");

  svg.append("text").attr("x", m.l).attr("y", m.t - 8).attr("fill", P.ink)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text("minimum landing reserve, winter doctrine");
}

/* ---------------------------------------------------------------
   Render, and re-render when the color scheme flips.
---------------------------------------------------------------- */
function renderAll() {
  const P = pal();
  ["fig-gap", "fig-discharge", "fig-reserve"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = "";
  });
  fig1(P); fig2(P); fig3(P);
}
renderAll();
if (window.matchMedia) {
  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  if (mq.addEventListener) mq.addEventListener("change", renderAll);
  else if (mq.addListener) mq.addListener(renderAll); // older Safari
}
