# The Ingest Gap: What Four Years of Sub-Zero FPV Combat Should Teach Canadian Arctic Force Modernization

*Camille Moreau · camilleelot.github.io*
*Draft v0.2 — analytical brief, target 2,800–3,200 words. Model: CGAI Policy Perspective / RUSI Newsbrief.*

> **Status of this draft:** Sections 1–5 are now drafted in full. Canadian-side citations were verified July 2, 2026: TR 2013-142 ✅, NRC icing series DOI ✅, TP 15263E (rev. 03/2025) ✅, MINDS TEG parameters ✅. One number remains open — the DRDC accession number for the Seto et al. 2013 CFJAE12 report — and is footnoted accordingly; the report itself is confirmed real via peer-reviewed secondary citation. Remaining pre-send items are listed at the end of this file.

---

## 1. Opening — the posture difference

On a Russian training-unit Telegram channel, a first-person-view drone instructor lays out the winter routine in five steps: waterproof the airframe in three layers, de-ice the motors with alcohol and let it flash off, drill flying in gloves, warm the batteries against the body before launch, and run a goggles-off visual check before the first flight of the day. The list is labelled with formal periodic-technical-service nomenclature — the same Soviet-era maintenance vocabulary once reserved for tanks and trucks. That label is the tell. The drone has been absorbed into the standard equipment fleet, and winter has been absorbed with it. Cold weather, in this corpus, is not a hazard to be flown around. It is a condition to be operated through.

Canada's published position on the identical question runs the other way. Under the Canadian Aviation Regulations, a small remotely piloted aircraft may not be flown when icing is observed, reported, or likely along the route unless it carries de-icing or anti-icing equipment or the pilot has a means to detect icing, and it may never be flown with frost, ice, or snow on its critical surfaces (CAR 901.35, as replaced by SOR/2025-70). The default posture is avoidance. The 2025 amendment is worth noting precisely because it *loosened* the rule — the 2019 version required both de-icing equipment and ice-detection equipment; the current version accepts either — yet even after a deliberate update, the regulatory frame remains one of staying out of the cold, not operating inside it.

This is not a content gap that more pages would close. It is a posture difference, and it is arguably the single most consequential thing Canada could extract from four years of sub-zero combat aviation in Ukraine.

The timing makes the gap expensive. Allied commentators now say plainly that the West is behind: a February 2026 *Defense News* assessment argues NATO is not ready for drone warfare in the Arctic, that Russia is institutionalizing its Ukraine combat lessons through a dedicated uncrewed-systems branch and mass operator training, and that allied doctrine, training, and innovation pathways have not kept pace. The same piece names the technical core of the problem — cold degrades batteries, icing attacks propulsion, and the alliance lacks systems certified for sustained cold-weather operation. NATO members are already responding at the tactical edge: Norwegian Arctic units are field-testing winterized FPV models, with Canadian special forces training alongside them at Cold Response 2026 (*Defense News*, March 2026). The proving ground is running. The lessons are being written down. Canada has no mechanism to read them.

## 2. The argument, and the scope guardrail

This brief does two things. First, it demonstrates an *ingest function* — the disciplined translation of frontline Russian- and Ukrainian-language technical doctrine into a form Canadian engineers and procurement officers can use — working end to end on a single subsystem: cold-weather power systems for tactical FPV-class UAS. Second, it argues that the ingest function itself, not any one finding, is the capability Canada should resource.

A scope guardrail belongs here, in the first 300 words, because the reflexive objection arrives early. Canada is *not* idle on Arctic drones. It has ordered eleven MQ-9B SkyGuardian remotely piloted systems and is flight-testing an Elbit Hermes 900 Starliner over the Arctic this season (CBC, April 2026). But those are medium-altitude, long-endurance, manufacturer-certified, cold-weather-hardened aircraft — the gap is not there. The gap is at the opposite end of the platform spectrum: the cheap, attritable, operator-built quadcopter that Russia and Ukraine field by the thousand and that Canada has no published cold-weather operating doctrine for at all. Everything that follows is scoped to that class, and the brief says so out loud so a reviewer cannot mistake the claim for one about the large programs.

The deeper point is structural. The Russia–Ukraine war has produced the largest sustained sub-zero combat-UAS proving ground in modern history, and its lessons are publicly available — in training-school decks, operator-education channels, and OEM production documentation — but they are written in Russian, distributed on Telegram, and wrapped in rhetorical framing that Western analysts either can't read or won't touch. The cost of leaving that corpus un-ingested is not abstract; it is paid every time a Canadian small-UAS requirement is written from first principles for a problem that two armies have already solved, badly and then well, in public.

---

## 3. Evidence — the ingest function demonstrated

What follows is the ingest function running end to end on one subsystem: electrical power in the cold — the batteries, motors, and consumables that decide whether an FPV-class aircraft flies at −20°C or sits in a case. All translations are the author's own. The source register, and the rules by which it was handled, close the section.

### 3a. Three winters, three stages

The corpus matures in public, and it matures the way industrial knowledge always has: improvisation, then aftermarket, then product.

The improvisation stage is visible in the earliest winter material and is easy to underestimate because it photographs like folklore. Operators smear pork fat on propeller blades as a crude anti-icing layer — a practice one Russian channel attributes to Ukrainian units, and which failed, in the same telling, when mice ate the propellers. Plastic bottles are slit and slid over battery packs as windbreaks. Chemical hand-warmers are taped to lithium packs before launch. Airframes dry in rows on apartment central-heating radiators between sorties. Homemade cardboard-and-wax trench candles heat the dugouts where all of this happens. None of it is doctrine. All of it is data: a fleet learning, at the individual-operator level, which failure modes winter actually produces.

The second stage replaces improvisation with named, purchasable consumables, and it is the stage at which the knowledge becomes legible to a procurement officer. Training channels recommend AERO LIGHT silicone conformal coating for flight-controller boards; АНТИЛЕД ("Anti-Ice"), a commercial de-icer spray; and B-7000, a Chinese transparent flexible sealant costing roughly three dollars a tube, pressed into service as a budget conformal coating. Commercial heated battery pouches appear across multiple channels. The fixes are the same fixes as stage one — keep water out, keep heat in — but they now have product names, prices, and application photos. That is what an aftermarket looks like when it forms around a real operational requirement.

The third stage is productization, and it runs from the bottom of the platform spectrum to the top. At the bottom: a tactical-equipment manufacturer partnering with an FPV training school on purpose-built operator gear — goggle cases, radio housings, battery carriers, a chest-mounted operator console — with the design sketches posted publicly. At the top: the Geran-2 strike drone's serialized "Зима" (Winter) kit — hermetic hatch sealing, pitot-tube heating, carburetor heating, engine intake screens — photographed with a production batch label dated March 2025 and reported through Ukrainian OSINT channels citing enemy sources. When winterization ships from the factory as a serialized module, the improvisation era is over.

The arc is the argument. Improvised fixes became commercial products became OEM modules, across three winters, in public. A corpus that matures this way is not folklore. It is doctrine formation, observable in real time — and everything observable is ingestible.

### 3b. The quantified core

The training material is specific enough to engineer against, which is what separates it from war-blog anecdote. An FPV school curriculum deck from 2023 states flatly that lithium-ion and lithium-polymer chemistry loses capacity in the cold and that "all electronics discharges at least 30% faster," and backs the claim with discharge curves plotted at −20°C, −10°C, 0°C, +23°C, and +45°C. At −20°C, useful capacity reads at roughly 30% of rated. The same deck sets a hard threshold on propulsion: below −15°C, brushless motors may fail to start at all, with time and charge consumed in self-heating. The logistics consequences are stated as requirements, not suggestions — a minimum of ten to fifteen batteries per drone in winter, and a pack that discharges overnight to zero is written off, an explicit disposal criterion.

Operator-education material from January 2026 adds the handling protocol around those numbers: bring a battery to +15…+20°C before installing it; give cold packs thirty to sixty minutes of room-temperature acclimation before charging; treat 3.0 volts per cell as a hard floor and 3.85 volts as storage voltage; and take off while the pack is still warm — a line that quietly converts battery temperature into operational tempo.

| Parameter | Value | Source class |
|---|---|---|
| Useful capacity at −20°C | ~30% of rated | FPV school deck, 2023 (single source) |
| BLDC cold-start failure threshold | below −15°C | FPV school deck, 2023 (single source) |
| Winter battery load-out | 10–15 packs per drone | FPV school deck, 2023 |
| Winter landing reserve | 40% (school, 2023) vs. 20–30% (operator channel, 2026) | divergent |
| Pre-install pack temperature | +15…+20°C | operator channel, Jan 2026 |
| Cell voltage floor / storage | 3.0 V / 3.85 V per cell | operator channel, Jan 2026 |

Two honesty flags belong on this table, and leaving them visible is the point. First, the discharge-curve figures and the −15°C threshold each trace to a single training-school slide; they are reported here as claims from that source, not as validated engineering data, and independent corroboration — precisely the kind of work the NRC's icing wind tunnel already does for propellers — is the natural next step. Second, the winter landing-reserve figure spreads from 20% to 40% across sources. That spread is itself a finding: Russian operator-facing winter doctrine is not fully consolidated. A Canadian equivalent should specify the number, not inherit the spread.

### 3c. The doctrinal tells

Three features of the corpus mark it as institutionalization rather than a collection of frontline tips.

The first is nomenclature, introduced in Section 1: the five-step winter checklist circulates under formal periodic-technical-service labelling, the maintenance paradigm that has governed Soviet and Russian fleet equipment for decades. Alongside it, training and procurement-adjacent material uses the phrase `всесезонность и всепогодность` — all-season and all-weather capability — a construction that mirrors NATO procurement language almost word for word. When the informal corpus starts speaking the vocabulary of requirements documents, it is converging on doctrine.

The second is curricular placement. Russian FPV school material teaches drone operation alongside mine awareness and terrain assessment — as a soldier skill, not a specialist trade. The Western pattern, in which small-UAS operation is a qualification held by designated personnel, is a different training-pipeline design with different scaling behaviour, and the divergence is worth naming when Canada designs its own.

The third is operator-builder pedagogy. The cadet builds the airframe, tunes it, and flies it — one person, one aircraft, one accountability loop. Western practice separates builder from operator. In southern conditions the separation is an efficiency argument; at a remote Canadian Arctic forward operating location, where resupply is measured in weeks, it becomes a capability argument. An operator who can field-rebuild and field-tune is not incrementally more valuable in the Arctic. The value multiplies with distance from the supply chain.

### 3d. Method

The source register spans three tiers, handled by different rules. The first tier is self-publicizing institutional channels — training schools and equipment manufacturers that post curriculum material, product photographs, and unit affiliations as recruitment and marketing content. These are treated as publishers, not protected sources: they are cited by channel, their claims are attributed, and no identification is added beyond what they publish about themselves — no cross-referencing of insignia to unit rosters, no naming of individuals visible in imagery, and no reproduction of photographs of identifiable persons. The second tier is aggregator and operator-education channels, handled identically. The third tier is human field observation, which informs the author's background understanding but carries no attributed claims in this brief; where such material is ever used, it is consented, pseudonymized, and stripped of locational detail.

Channels carry identifiable political orientations, and the rhetorical framing — bravado captions, culture-war asides — is recorded as evidence of posture ("we are not afraid of the frost" is itself a doctrinal statement) but separated from technical content, which is evaluated on internal consistency and cross-channel agreement. Translations are the author's own. Quantitative claims resting on a single source are marked as such above.

---

## 4. The Canadian baseline — the gap, precisely drawn

The Canadian published record on small-UAS cold-weather operations is real, serious, and old. Read in sequence, it draws the gap more sharply than any outside critique could.

The experimental baseline is CF Joint Arctic Experimentation 2012, a joint capability-development experiment conducted in and around Gascoyne Inlet, Nunavut, in August 2012, reported by Seto and colleagues at DRDC the following year.¹ The findings read as a catalogue of unsolved small-platform problems: the fixed-wing UAV could not be safely operated from rough Arctic ground; the quadrotor was lost after its second flight; navigation was hampered by high-latitude magnetic effects, prompting the recommendation that northern UAV operations not rely on stable magnetic heading. The report's own gap statement is the important one — no formal small-UAS Arctic SOP annex existed, and procedures had to be extrapolated from lessons learned.

The capability-analysis baseline is DRDC Ottawa's 2013 Arctic surveillance study (Brookes, Scott, and Rudkin, TR 2013-142), which compared manned platforms with small remotely piloted aircraft for Arctic surveillance and concluded that small UAVs "must still prove their capabilities in the harsh Arctic environment." The study anticipated that winter land surveillance might require operation down to −50°C, flagged wind buffeting and thrust-margin limits, and positioned small UAVs as tactical adjuncts pending Arctic trials. It is a careful document. It is also a CONOPS document — by its own account it contains no cold-weather procedures, no battery management, no de-icing protocol.

The scientific and regulatory baseline is the most current, and it is prohibition-shaped by design. The National Research Council's multi-phase investigation of icing tolerance for small UAV rotors and propellers (Phase 2: DOI 10.4224/40002002; the series runs through Phase 4, with companion results published at AIAA in 2021) characterized how quickly ice accretion degrades thrust on small propellers at high RPM. That work is the evidentiary basis for the regulatory position described in Section 1: under CAR 901.35 and the knowledge requirements of TP 15263E (revised March 2025), the small RPAS is normatively a no-icing aircraft. The science says small rotors ice fast; the regulation says stay out of icing; and both are correct within their frame.

The gap, then, is not that Canada has ignored the problem. It is that the newest item in this record predates the FPV revolution, the record's operational layer dates to 2012–2013, and the entire corpus answers the question "when should a small drone not fly?" while the Russian-language corpus answers "how does a small drone fly anyway?" Between the eleven-aircraft MQ-9B program at one end of the spectrum and the no-icing consumer quadcopter at the other sits the attritable tactical class that two armies have spent four winters operating — and for that class, on the Canadian side, there is nothing to cite.

## 5. Recommendation — resource the ingest function

This brief is the proof of concept, deliberately narrow: one subsystem, one platform class, one analyst-winter of open sources. The recommendation is not any finding above. It is the function that produced them.

Canada should resource a sustained ingest capability: a small, standing translation-and-analysis effort that reads the Russian- and Ukrainian-language operational corpus as it is published and delivers subsystem-level briefs — power systems, optics, fiber-optic control, counter-UAS — into the hands of the engineers writing Canadian small-UAS requirements and the officers writing Canadian cold-weather doctrine. The unit of output is the brief, not the database; the standard of evidence is the one demonstrated in Section 3d, with source tiers, framing separated from content, and single-source claims marked.

The natural funding vehicle is the MINDS program's Targeted Engagement Grants, which provide non-recurring support of up to $50,000 for research and publications aligned with DND/CAF policy priorities, applied for through an affiliated university, not-for-profit, or research institution. The framing matters: MINDS privileges policy relevance and explicitly redirects technically scoped proposals toward IDEaS, so the ingest function should be presented as what it is — knowledge mobilization that informs procurement policy, training-pipeline design, and doctrine — with deep technical validation, such as corroborating the discharge-curve claims in Section 3b, delivered through DRDC tasking or NRC's existing icing program. MINDS' Rapid Response Mechanism offers a secondary route when the requirement moves faster than a grant cycle. Any application should be aligned against the current MINDS Defence Policy Challenges before submission.

The cost asymmetry is the closing argument. The corpus is open. The proving ground is funded by someone else. The only barrier is language, and the price of leaving the barrier standing is paid in Canadian requirements written from first principles for problems already solved — badly, then well, in public — by the two armies with the most sub-zero drone combat experience in history. An analyst who reads Russian, a grant measured in tens of thousands of dollars, and a publication cadence of one subsystem per quarter would close it. This brief is what one quarter looks like.

---

### Citation register (updated July 2, 2026)

| Source | Type | Status |
|---|---|---|
| CAR 901.35 (as replaced by SOR/2025-70) | Regulatory | ✅ confirmed (prior session) |
| TP 15263E, *Knowledge Requirements for Pilots of RPAS, 250 g up to and including 150 kg, Basic and Advanced Operations*, rev. 03/2025 | Regulatory | ✅ confirmed on TC site — cite revision date, not "4th ed." |
| Seto et al., *CF Joint Arctic Experimentation 2012 – Potential use of UXVs in CF Arctic Operations*, DRDC, 2013 | Primary (experiment report) | ✅ report confirmed real via *The Geographical Journal* (doi 10.1111/geoj.12533), which quotes scope and dates. ⚠️ Accession number ("TM 2013-003") unconfirmed — check DRDC publications portal directly; cite by author/title/year if not resolved.¹ |
| Brookes, Scott & Rudkin, *Arctic Surveillance: Civilian Commercial Aerial Surveillance Options for the Arctic*, DRDC Ottawa TR 2013-142 | Secondary (capability analysis) | ✅ confirmed — GC Publications catalogue D68-4/142-2013E-PDF |
| NRC, *Investigation of tolerance for icing of small UAV rotors/propellers*, Phase 2, DOI 10.4224/40002002 (series Phases 1–4; AIAA companion paper 10.2514/6.2021-2675) | Secondary (technical) | ✅ confirmed — DOI resolves; NRC Publications Archive |
| *Defense News* (NATO Arctic drone readiness, Feb 2026; Norway FPV / Cold Response, Mar 2026) | Secondary | ✅ confirmed (prior session) |
| CEPA, *High Stakes in the High North* (Feb 2026) | Secondary context | ✅ confirmed (prior session) |
| MINDS Targeted Engagement Grants (parameters, eligibility, IDEaS boundary) | Program | ✅ confirmed on canada.ca — current intake closed, decisions due end July 2026 |
| FPV_выZOV; Two Majors; mil_hub; Техник БПЛА; notes_veterans; getyourdrone; FPV school 2023 deck | Primary (RU-language) | ⚠️ **recover t.me/ URLs from your PC** — register incomplete without them |

¹ Footnote for the brief itself: "Report accession number pending confirmation against the DRDC publications portal; cited here by author, title, and year."

### Remaining pre-send checklist

1. Recover Telegram t.me/ URLs for every cited post (only you can do this — your screenshots, your archive).
2. DRDC publications portal lookup for the Seto et al. accession number; if it resolves, replace footnote 1 with the number.
3. Image pass on the visual archive: strip EXIF, no identifiable faces, describe rather than reproduce anything with fuzzy provenance or rights; redraw the discharge-curve and kit-list slides as your own figures rather than reposting them.
4. Check current MINDS Defence Policy Challenges list; adjust one sentence in Section 5 if there's an exact Arctic/continental-defence challenge to name.
5. Read-aloud pass on Sections 3–5 in your own voice; adjust anything that doesn't sound like you.
