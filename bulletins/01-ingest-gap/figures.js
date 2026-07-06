/* Figures for "The Ingest Gap" — bulletin 01.
   Each figure renders only if its container div exists, so this one file
   drives both index.html (the brief) and figures.html (the workbench).
   Requires d3 v7 to be loaded first. */

const INK = "#111", FAINT = "#999", COLD = "#3b6e8f"; // one accent: frontline corpus only

/* ---------------------------------------------------------------
   FIGURE 1 — The Ingest Gap timeline
   Canadian dots: verified items only.
   Frontline ticks: dated from findings doc; d ≈ approximate → adjust
   from the Telegram archive when the t.me URLs are recovered.
---------------------------------------------------------------- */
const CAN = [
  {d: 2012.6, label: "CFJAE12, Gascoyne Inlet"},
  {d: 2013.5, label: "DRDC TR 2013-142"},
  {d: 2019.4, label: "CARs Part IX · TP 15263"},
  {d: 2020.3, label: "NRC icing series, Ph. 1–4"},
  {d: 2025.2, label: "SOR/2025-70 · TP 15263E rev."}
];
const RU = [ // {d, s: stage 1|2|3, label (optional, only majors get text)}
  // dates marked "verified" are pinned by t.me embed pages (July 5, 2026);
  // the rest remain approximate pending URL recovery
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

(function fig1(){
  if (!document.getElementById("fig-gap")) return;
  const W = 860, H = 330, m = {t: 28, r: 30, b: 46, l: 30};
  const svg = d3.select("#fig-gap").append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`).attr("width", "100%");
  const x = d3.scaleLinear().domain([2011.8, 2026.7]).range([m.l, W - m.r]);
  const yCAN = 78, yRU = 190;

  // time axis — years as bare numbers, no domain line heavier than a hair
  const ax = d3.axisBottom(x).tickValues(d3.range(2012, 2027, 2))
    .tickFormat(d3.format("d")).tickSize(4);
  svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(ax)
    .call(g => { g.select(".domain").attr("stroke", FAINT);
                 g.selectAll("text").attr("fill", "#444").style("font-size", "11px");
                 g.selectAll("line").attr("stroke", FAINT); });

  // Feb 2022 hairline
  svg.append("line").attr("x1", x(2022.12)).attr("x2", x(2022.12))
    .attr("y1", m.t).attr("y2", H - m.b).attr("stroke", FAINT)
    .attr("stroke-dasharray", "2,3");
  svg.append("text").attr("x", x(2022.12)).attr("y", m.t - 8)
    .attr("text-anchor", "middle").attr("fill", "#555").style("font-size", "10.5px")
    .style("font-style", "italic").text("Feb 2022 — the FPV revolution begins");

  // track labels
  svg.append("text").attr("x", m.l).attr("y", yCAN - 34).attr("fill", INK)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text("canadian published corpus");
  svg.append("text").attr("x", m.l).attr("y", yRU + 4).attr("fill", COLD)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text("russian / ukrainian frontline corpus");

  // Canadian dots + stacked labels (alternate above/below to avoid collision)
  svg.selectAll(".can").data(CAN).join("circle")
    .attr("cx", d => x(d.d)).attr("cy", yCAN).attr("r", 4.5)
    .attr("fill", "none").attr("stroke", INK).attr("stroke-width", 1.4);
  svg.selectAll(".canl").data(CAN).join("text")
    .attr("x", d => x(d.d)).attr("y", (d, i) => yCAN + (i % 2 ? 22 : -14))
    .attr("text-anchor", "middle").attr("fill", "#333").style("font-size", "10.5px")
    .text(d => d.label);

  // frontline ticks — density is the argument
  svg.selectAll(".ru").data(RU).join("line")
    .attr("x1", d => x(d.d)).attr("x2", d => x(d.d))
    .attr("y1", yRU - 11).attr("y2", yRU + 11)
    .attr("stroke", COLD).attr("stroke-width", 2.1).attr("opacity", .9);
  // labeled majors — the labels cluster over 2022–2026, so each gets its own row
  const majors = RU.filter(d => d.label);
  svg.selectAll(".rul").data(majors).join("text")
    .attr("x", d => x(d.d))
    .attr("y", (d, i) => yRU - 18 - i * 12)
    .attr("text-anchor", d => d.d > 2025.6 ? "end" : "middle")
    .attr("fill", "#2c536b").style("font-size", "10px")
    .text(d => d.label);

  // stage brackets beneath the frontline track
  STAGES.forEach(s => {
    const y = yRU + 26 + (s.t.startsWith("2") ? 14 : s.t.startsWith("3") ? 28 : 0);
    svg.append("line").attr("x1", x(s.a)).attr("x2", x(s.b))
      .attr("y1", y).attr("y2", y).attr("stroke", "#7a97a8").attr("stroke-width", 1);
    svg.append("text").attr("x", x(s.a)).attr("y", y - 3).attr("fill", "#5b7889")
      .style("font-size", "9.5px").style("font-style", "italic").text(s.t);
  });
})();

/* ---------------------------------------------------------------
   FIGURE 2 — discharge scaffold. Curves render ONLY from real data.
   DISCHARGE_DATA: fill each series with {t: tempC, c: capacityPct}
   points transcribed from the FPV-school slide. Leave empty = the
   figure shows frame + verified anchors + "awaiting transcription".
---------------------------------------------------------------- */
const DISCHARGE_DATA = [
  // Author's eyeball transcription (July 6, 2026) of the deck's
  // voltage-vs-capacity curve family, read at the 3.0 V cutoff and
  // normalized to the +45°C curve (~2000 mAh ≈ rated).
  // VERIFY against the slide pixels before publication.
  { name: "deck curves, % of rated (author's reading)",
    pts: [{t: -20, c: 54}, {t: -10, c: 82}, {t: 0, c: 95}, {t: 23, c: 97}, {t: 45, c: 100}] }
];
const VERIFIED_ANCHORS = [
  {t: -20, c: 54, label: "≈54% of rated at −20°C (deck curves, 2023)"}
];

(function fig2(){
  if (!document.getElementById("fig-discharge")) return;
  const W = 620, H = 300, m = {t: 26, r: 30, b: 44, l: 52};
  const svg = d3.select("#fig-discharge").append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`).attr("width", "100%").style("max-width", "620px");
  const x = d3.scaleLinear().domain([-30, 45]).range([m.l, W - m.r]);
  const y = d3.scaleLinear().domain([0, 100]).range([H - m.b, m.t]);

  const axX = d3.axisBottom(x).tickValues([-30, -20, -15, -10, 0, 23, 45])
    .tickFormat(d => d + "°").tickSize(4);
  const axY = d3.axisLeft(y).tickValues([0, 30, 50, 100])
    .tickFormat(d => d + "%").tickSize(4);
  svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(axX)
    .call(g => { g.select(".domain").attr("stroke", FAINT);
                 g.selectAll("text").attr("fill", "#444").style("font-size", "11px");
                 g.selectAll("line").attr("stroke", FAINT); });
  svg.append("g").attr("transform", `translate(${m.l},0)`).call(axY)
    .call(g => { g.select(".domain").remove();
                 g.selectAll("text").attr("fill", "#444").style("font-size", "11px");
                 g.selectAll("line").attr("stroke", FAINT); });

  // −15°C cold-start threshold
  svg.append("line").attr("x1", x(-15)).attr("x2", x(-15))
    .attr("y1", y(100)).attr("y2", y(0)).attr("stroke", "#8a5a00")
    .attr("stroke-dasharray", "2,3");
  svg.append("text").attr("x", x(-15) - 6).attr("y", y(88))
    .attr("text-anchor", "end").attr("fill", "#8a5a00").style("font-size", "10px")
    .style("font-style", "italic").text("BLDC cold-start threshold −15°C");

  // verified anchor(s)
  VERIFIED_ANCHORS.forEach(a => {
    svg.append("circle").attr("cx", x(a.t)).attr("cy", y(a.c)).attr("r", 4.5)
      .attr("fill", COLD);
    svg.append("text").attr("x", x(a.t) + 9).attr("y", y(a.c) + 4)
      .attr("fill", "#2c536b").style("font-size", "10.5px").text(a.label);
  });

  if (DISCHARGE_DATA.length === 0) {
    svg.append("text").attr("x", (x(-30) + x(45)) / 2).attr("y", y(72))
      .attr("text-anchor", "middle").attr("fill", "#999")
      .style("font-size", "12px").style("font-style", "italic")
      .text("curves render when DISCHARGE_DATA is transcribed from the source slide");
  } else {
    const line = d3.line().x(p => x(p.t)).y(p => y(p.c)).curve(d3.curveMonotoneX);
    DISCHARGE_DATA.forEach(s => {
      svg.append("path").attr("d", line(s.pts)).attr("fill", "none")
        .attr("stroke", COLD).attr("stroke-width", 1.6);
      svg.selectAll(null).data(s.pts).join("circle")
        .attr("cx", p => x(p.t)).attr("cy", p => y(p.c)).attr("r", 2.5)
        .attr("fill", COLD);
      const last = s.pts[s.pts.length - 1];
      // series ends at the right edge, so the label anchors end, below the curve
      svg.append("text").attr("x", x(last.t)).attr("y", y(last.c) + 16)
        .attr("text-anchor", "end")
        .attr("fill", "#2c536b").style("font-size", "10px").text(s.name);
    });
  }
  svg.append("text").attr("x", m.l).attr("y", m.t - 10).attr("fill", INK)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text("useful capacity vs. ambient temperature");
})();

/* ---------------------------------------------------------------
   FIGURE 3 — landing-reserve spread (real values, two sources)
---------------------------------------------------------------- */
(function fig3(){
  if (!document.getElementById("fig-reserve")) return;
  const W = 620, H = 150, m = {t: 24, r: 40, b: 34, l: 40};
  const svg = d3.select("#fig-reserve").append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`).attr("width", "100%").style("max-width", "620px");
  const x = d3.scaleLinear().domain([0, 50]).range([m.l, W - m.r]);
  const y = H - m.b - 34;

  const ax = d3.axisBottom(x).tickValues([0, 10, 20, 30, 40, 50])
    .tickFormat(d => d + "%").tickSize(4);
  svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(ax)
    .call(g => { g.select(".domain").attr("stroke", FAINT);
                 g.selectAll("text").attr("fill", "#444").style("font-size", "11px");
                 g.selectAll("line").attr("stroke", FAINT); });

  // winter spread band 20–40
  svg.append("line").attr("x1", x(20)).attr("x2", x(40)).attr("y1", y).attr("y2", y)
    .attr("stroke", COLD).attr("stroke-width", 5).attr("opacity", .35);
  // endpoints — staggered vertically so the two labels can't collide mid-band
  [[20, "operator channel, Jan 2026: 20–30%", "start", 12], [40, "training deck, 2023: 40%", "end", 26]]
    .forEach(([v, t, anch, dy]) => {
      svg.append("circle").attr("cx", x(v)).attr("cy", y).attr("r", 4).attr("fill", COLD);
      svg.append("text").attr("x", x(v)).attr("y", y - dy)
        .attr("text-anchor", anch === "end" ? "end" : "start")
        .attr("fill", "#2c536b").style("font-size", "10.5px").text(t);
    });
  // summer comparator
  svg.append("circle").attr("cx", x(20)).attr("cy", y + 22).attr("r", 4)
    .attr("fill", "none").attr("stroke", INK).attr("stroke-width", 1.4);
  svg.append("text").attr("x", x(20) + 9).attr("y", y + 26).attr("fill", "#333")
    .style("font-size", "10.5px").text("typical summer reserve: 20%");
  svg.append("text").attr("x", m.l).attr("y", m.t - 8).attr("fill", INK)
    .style("font-size", "12px").style("font-variant", "small-caps")
    .text("minimum landing reserve, winter doctrine");
})();
