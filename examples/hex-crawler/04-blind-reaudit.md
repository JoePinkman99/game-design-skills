# War Wheel — Deep Design Audit

*Method: game-analysis skill, Path B (read-and-extract), deep audit. Material examined: `war-wheel-spec.md` only, per instruction — no other workspace files were read; this is a cold, independent re-audit. Matrix layer diagnosed before any spatial/tempo/information claim (standing rule 1); framework claims attributed to reference sections; scripts run: `matrix_analysis.py` (stack 2 and 3), plus scratch enumerations of the 35×35 army layer, a single-edge-flip probe, and an exhaustive 2²¹ tournament sweep.*

## 1. Game snapshot

**War Wheel** (working name): the tactical layer of a hex-grid strategy game. Two players, symmetric; each drafts 4 distinct archetypes from a shared roster of 7 seated on a wheel (Pikemen, Cavalry, Archers, Siege, Fliers, Mages, Infantry); each unit beats the units 1, 2, and 4 seats clockwise. Combat is chart-decided; information is fully open; turns are sequential; victory is destroying or breaking the enemy army.

Confidence: **exact** on everything chart- and draft-shaped — the interaction table was verified edge-by-edge against the generative rule (all 21 edges agree) and all army-layer claims are full enumerations, not samples. **Conditional** on everything spatial/tempo-shaped — movement and attrition numbers are a declared tuning layer, and several base-loop inheritances are unspecified (see §7).

## 2. Typology

| Axis | Verdict | Evidence |
|------|---------|----------|
| Transitive / intransitive | **Intransitive — maximally so** | Script: cycle exists; **14 three-cycles = the theoretical maximum** (n³−n)/24 for n=7; no dominated nodes |
| Simultaneous / sequential | **Sequential** (battle); draft protocol unspecified | Spec: "turns are sequential as in the base loop"; draft simultaneity undeclared → §7 |
| Symmetric / asymmetric | **Symmetric** | Identical roster both sides; perfectly antisymmetric W/L chart; mirrors even |
| Spatial / abstract | **Spatial** | Hex grid; maneuver-to-engage; range-2 Siege, pass-over Fliers, splash Mages |
| Dense / sparse matrix | **Dense — complete tournament** | All 21 off-diagonal pairs decisive; zero neutral outcomes (the base loop had two neutral pairs) |

Framing: a deterministic, perfect-information hex-tactics duel built on an intransitive counter-wheel — a chess-like body on an RPS heart. Per interaction-structure.md §1.2, the simultaneous-read pillar cannot live in the sequential battle; if it lives anywhere, it lives in the pre-battle draft.

## 3. Systems map

**Core loop:** draft 4-of-7 (35 armies) → deploy → alternate sequential maneuver on hexes → force engagements → chart resolves the exchange in the winner's favor (mirrors even) → attrition accrues (inherited) → destroyed/broken army loses.

**Node set (7):** Pikemen, Cavalry, Archers, Siege, Fliers, Mages, Infantry — wheel order; each beats seats +1, +2, +4 clockwise.

**Interaction matrix** (verified ≡ generative rule, all 21 edges):

|  | Pik | Cav | Arc | Sie | Fli | Mag | Inf |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Pikemen** | — | W | W | L | W | L | L |
| **Cavalry** | L | — | W | W | L | W | L |
| **Archers** | L | L | — | W | W | L | W |
| **Siege** | W | L | L | — | W | W | L |
| **Fliers** | L | W | L | L | — | W | W |
| **Mages** | W | L | W | L | L | — | W |
| **Infantry** | W | W | L | W | L | L | — |

This is the quadratic-residue (Paley) tournament on 7 vertices — {1,2,4} are the QRs mod 7. Legacy compatibility: all four base-loop edges survive (Pikemen>Cavalry, Cavalry>Archers, Archers>Infantry, Infantry>Pikemen) and the two old neutral pairs are resolved (Pikemen>Archers, Infantry>Cavalry) — a veteran's knowledge transfers intact.

**Economy:** none at this layer, by declaration. Consequence worth naming: no faucet/sink also means no built-in tempo pressure — nothing economic ever forces a player to engage (feeds Finding T1).

**Progression gates:** none — single-battle scope; campaign layer out of scope by declaration.

## 4. Fun engines (ranked)

1. **Positional planning** — interaction-structure.md §2.3/§3.2 — *evidence:* the chart is maximally cyclic, so every approach vector touches a live edge; three spatial hooks (range-2, pass-over, splash) make space non-cosmetic — *sustains:* rich matrix + meaningful space + tempo limits — *kills:* engagement-refusal (kiting) collapsing the planning tree; stalemates — **health: healthy, conditional on T1/T2 below.**
2. **Prediction loop, relocated to the draft** — interaction-structure.md §1 — *evidence:* 35-comp selection over a strongly connected, EV-zero meta (enumerated) — *sustains:* blind simultaneous picks; iteration across a series (§2.1) — *kills:* open/sequential drafting (engine vanishes into counter-pick calculus). The in-battle absence of simultaneity is **N/A by genre** (fun-engines.md genre note), not a defect — **health: at risk, pending the draft-protocol ruling (I1).**
3. **Pattern mastery** — Koster, *A Theory of Fun* — *evidence:* one wheel rule generates all 21 edges; the army classes (anvil / hunter / mixed, §5-M1) are a discoverable meta-vocabulary with distinct risk personalities — *sustains:* layered discoverables — *kills:* onboarding hump; two theme-dissonant edges resist fiction-chunking (Y2) — **health: healthy, with an onboarding watch-item.**
4. **Challenge** — MDA — *evidence:* symmetric, zero-randomness skill duel; natural ranked play — *sustains:* 630 unordered draft matchups plus hex-map variety — *kills:* solved openings at the elite ceiling (systemic-levers.md, randomness placement) — **health: healthy short/medium term; at risk at the far ceiling (Y1).**

## 5. Diagnosis

### Matrix layer — what the script verifies (verbatim findings first)

`matrix_analysis.py` on the 7×7 chart: **Tournament: yes** · **INTRANSITIVE (cycle exists)** · **3-cycles: 14** · **Dominated nodes: none** · **size 2: none — the 2-Paradox property holds** · eigenvector viability **uniform 0.1429 (=1/7)** across all seven units.

Beyond the script, three exact results from scratch enumerations:

- **Uniqueness.** Of all 2,097,152 tournaments on 7 nodes, exactly 240 labeled ones are 2-paradoxical, and they form **one isomorphism class — this wheel**. The chart is not one good option among many; it is *the* unique 7-node solution, at the mathematically minimal roster size (interaction-structure.md Query 4).
- **Army layer is balanced at EV.** All 35 armies have total sum-score exactly 0 across the field; no army is dominated; no army is unbeaten; the 35-army digraph is strongly connected (the metagame is itself fully intransitive — no counter-pick sink). Because any two armies share ≥1 archetype (4+4 > 7), blowouts are capped at ±4 of a theoretical ±16 — draft matchups are structurally close.
- **Doom-stack landscape.** No unbeatable pair (every duo has exactly one common counter — the doubly-regular λ=1 property). 28 of 35 triples have no single-unit counter, which is **forced at n=7** (a 3-Paradox needs ≥19 nodes) — see structural notes.

**Design goals validated:** no dominant unit, no invincible pair, minimal roster for the property, legacy 4-cycle preserved, old neutrals resolved, perfectly uniform viability. The redesign's stated math lever landed exactly.

### Live issues

**[Tempo] T1 — Engagement-forcing is the load-bearing wall — High.**
Every balance result above is conditional on engagements actually happening. In a sequential, perfect-information, deterministic game, no one voluntarily initiates a losing engagement — a chart edge converts to attrition only when the winner can *force* contact. The spec provides no tempo forcer at this layer: no economy, no map objectives, no turn limit. The declared speed spread then re-weights the chart: a faster chart-loser refuses contact indefinitely; a faster chart-winner engages at will. Worst case is mutual refusal — stalemate non-games. The spec inherits "maneuvering to force engagements" from the base loop; whether the base loop actually contains forcing machinery (zones of control, disengage penalties) is an assumption this audit cannot verify (§7-A2).

**[Spatial] T2 — Fliers are the most tuning-sensitive unit — High, pending tuning.**
Fastest movement + pass-over means Fliers' three chart losses (Pikemen, Archers, Siege — all plausibly slower) are the most *refusable* in the game, while their three wins (Cavalry, Mages, Infantry) are the most *forcible*; pass-over specifically defeats body-blocking, the standard spatial counter to a fast diver. At the tempo layer their effective row trends toward "three forcible wins, three refusable losses." In-spec counterweights exist — Siege's range-2 bubble is area denial Fliers can't dodge by speed, Mage splash punishes clustering, mirror Fliers trade evenly — but the whole balance rests on movement numbers, i.e. the deliberately unspecified layer. This is where the design most likely breaks in playtest.

**[Information] I1 — Draft protocol unspecified — Medium.**
Blind-simultaneous vs open-sequential drafting decides whether the game has a psychological engine at all (engine 2). Open drafting also hands the second picker a free structural edge every match: the meta is strongly intransitive, so there is no absolute best army, but a per-matchup sign advantage is always available to whoever picks last.

**[Matrix→draft texture] M1 — Class tilt: anvils over hunters — Medium-Low.**
The 35 armies fall into exactly three structural classes under the wheel's symmetry group, with enumerated sign-records (out of 34):

| Class | Form | n | Record | Win margins |
|-------|------|---|--------|-------------|
| **ANVIL** | a unit + the 3 that beat it | 7 | **19-0-15** | avg win +1.58, avg loss −2.00 |
| **HUNTER** | a unit + the 3 it beats | 7 | **15-0-19** | avg win +2.00, avg loss −1.58 |
| **MIXED** | everything else | 21 | **14-6-14** | symmetric, ±4 extremes |

Margins exactly compensate — every army's EV is 0 — so this is texture, not imbalance: anvils are the consistent pick (many shallow wins), hunters the boom-bust pick (few deep wins), mixed the swingy peer-fight pick (all ±4 blowouts *and* all 63 ties are MIXED-vs-MIXED). The bite: **HUNTER(w) can answer an enemy *w* only with a mirror trade** — its one coverage hole, live in 133/1190 matchups (11.2%); the perfect-maneuver matching model confirms hunters cap at 3-of-4 favorable pairings in exactly those 133. If players track sign-winrate rather than EV, drafts drift anvil-ward (anvils also edge hunters head-to-head, 28-21).

**[Spatial] S1 — Mage splash vs the chart is ambiguous — Medium-Low.**
"Splash one hex adjacent to the target" doesn't say whether the chart governs splash victims. If splash chips units that *beat* Mages, Mages gain off-chart damage — a stealth matrix edit smuggled in through the spatial layer, softening the tournament purity everything else preserves. One ruling sentence fixes it.

**[Systemic] Y1 — Elite-horizon solvability — Low-Medium.**
Deterministic + symmetric + perfect information → solved openings at the far ceiling (systemic-levers.md: "zero randomness in symmetric games produces solved openings"). Draft variety and hex-map size defer this a long way; they don't eliminate it.

**[Systemic] Y2 — Onboarding load of 21 decisive edges — Low.**
Seven nodes is within the Query-1 cognitive budget and the wheel rule compresses hard, but players memorize charts through fiction, and two edges resist it: **Siege>Fliers** (strong dissonance — catapults swatting agile flyers) and **Pikemen>Archers** (mild — and it was neutral in the base loop). These will be the two most-forgotten edges in play.

### Structural notes (true but inert, or discipline)

- **28/35 triples uncounterable by a single unit is mathematically forced at n=7** (3-Paradox needs ≥19 nodes). Roster expansion would be the wrong fix — it trades an unavoidable property for a Query-1 cognitive-load violation. Counterplay correctly lives at engagement granularity, which is exactly what the spatial layer is for.
- **The chart is rigid — never patch by edge surgery.** Flipping even the most thematically awkward edge (Siege>Fliers) creates two doom-pairs ({Pikemen, Fliers}, {Fliers, Mages}) and breaks regularity (Fliers 4W, Siege 2W); by the uniqueness result, *any* edit whatsoever destroys the 2-Paradox property. Theme problems get fiction fixes, not edge flips.
- **Mirrors are always live:** any two armies share ≥1 archetype, so mirror-attrition semantics (both chip? both die?) matter in every single match — more than their one-line treatment in the spec suggests (§7-A5).
- The 63 sum-tied matchups (all MIXED-vs-MIXED) are pure maneuver-decided games — that's where you want ties to live.

## 6. Improvement levers (smallest sufficient, per finding)

- **T1 → add a default engagement forcer.** Two candidates, either alone may suffice: (a) *disengage attrition* — breaking adjacency with an enemy costs a small chart-independent chip; (b) a *default objective* — holding central hexes wins a timed/tiebroken game. Predicted effect: speed converts from an engagement-veto into engagement-currency; chart edges become realizable; stalemates impossible by construction. Cost: +1–2 rules, low cognitive load. Risk: over-punishing movement collapses the positional-planning engine — tune gently.
- **T2 → treat as a tuning watch-item with a named metric** (Flier pick/win rate per matchup). Primary lever is movement numbers (shrink the speed gap; make pass-over cost extra movement). Fallback, one rule: flying over or adjacent to a unit that beats Fliers grants that unit a free chip strike ("ground fire"). Cost: one rule; preserves Flier identity.
- **I1 → rule the draft blind & simultaneous.** For organized play, best-of-N with re-drafts between games — the iteration lever (interaction-structure.md §2.1) — so behavioral reads accumulate across the series. Cost: zero in-battle load.
- **M1 → no action now; monitor.** If anvil sign-winrate sustains >55% in playtests, compensate spatially (e.g., hunter-class armies deploy second, seeing one enemy placement) — never via chart edits (see rigidity note). Cost today: none.
- **S1 → one ruling sentence:** splash applies the chart relation of Mages vs each splashed unit — it chips only units Mages beat, and does nothing to mirrors or counters. Effect: tournament purity preserved, AoE identity intact.
- **Y1 → input randomness only, placed before decisions** (Engelstein placement, systemic-levers.md): varied maps/terrain drawn before deployment. No output dice — deterministic resolution is part of this design's identity. Cost: content authoring.
- **Y2 → re-fiction, zero mechanics.** Recast Siege as bolt-thrower/ballista batteries — anti-air fiction makes Siege>Fliers intuitive; narrate Pikemen>Archers as the braced, shield-covered advance arrows can't stop. Effect: the two worst edges become memorable; onboarding cost drops.

## 7. Assumptions & open questions

- **A1 — Draft protocol** assumed blind-simultaneous (spec silent). Finding I1 and fun engine 2 hinge on this.
- **A2 — Base-loop inheritances** taken on faith and unspecified here: engagement-forcing machinery (ZOC, disengage rules), attrition numbers, army-break threshold, activation structure (alternating single-unit vs whole-army turns).
- **A3 — Legacy-four spatial profile** unspecified: in particular, do Archers attack at range? If yes, that's a fourth engagement-forcing asymmetry this audit couldn't score.
- **A4 — Fliers:** attacks-of-opportunity while passing over? What happens when all landing hexes are occupied?
- **A5 — Mirror resolution** "even": assumed simultaneous mutual attrition with no positional winner.
- **A6 — Map size/terrain** unspecified — kiting severity (T1/T2) scales with open ground.
- **A7 — Numeric tuning layer** deliberately out of scope per the spec: all [Tempo]/[Spatial] findings are conditional; all [Matrix] findings are exact enumerations.
- **A8 — Campaign layer** out of scope by declaration.

---

**Bottom line.** The mathematical core is as good as this construction can possibly be — provably unique, maximally cyclic, uniform-viability, doom-stack-free at pairs, EV-balanced across all 35 drafts with real strategic texture (anvil/hunter/mixed personalities) and a fully intransitive metagame. The design's actual risk surface is entirely in what the spec leaves to inheritance and tuning: whether engagements can be forced at all (T1), whether Flier speed lets them opt out of their own column (T2), and three one-sentence ambiguities (draft protocol, splash-vs-chart, mirror semantics). Fix those with the small levers above and the wheel should hold in play as well as it holds on paper.
