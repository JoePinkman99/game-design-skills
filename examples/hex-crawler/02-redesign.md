# Hex-Crawler Tactical Combat Loop — Redesign Proposals

**Status: theory-consistent, not play-tested.**
Seeded by [hex-crawler-combat-analysis.md](hex-crawler-combat-analysis.md)
(2026-07-08 audit of the four-unit combat loop). All charts verified with the
game-analysis skill's `matrix_analysis.py`; script output quoted verbatim
(elisions marked `[…]`).

## 1. Design brief (echo)

**Identity pillars** (audit §2 + §4):

1. **Sequential turn resolution** — turn-based hex crawler, HoMM / Fire
   Emblem / Total War lineage (audit §2).
2. **Spatial hex maneuver as the enrichment layer** — flanking, movement,
   forcing favorable matchups over several turns (audit §2, §3;
   interaction-structure §2.3).
3. **Intransitive archetype counter-web as the interaction core** — the
   4-cycle Infantry → Pikemen → Cavalry → Ranged → Infantry (audit §2, §3).
4. **Symmetric roster, flat viability** — both sides draw the same
   archetypes; centrality 0.2500 each (audit §2).
5. **Low cognitive load** — 6 pairwise matchups today; the audit's own
   ceiling talk puts ~7 nodes / 21 matchups at the top of the comfortable
   range (audit §5 Finding 5; interaction-structure Query 1).

**Defining engine to restore:** audit §4 #1, "Prediction loop (spatial
variant)" — in the current fun-engines taxonomy this is **Positional
planning**, the sequential+spatial genre's native engine (fun-engines.md,
genre-fit note). One refinement carried through this doc: per that note,
missing simultaneity is N/A by genre, *not* a defect — so the engine's
"broken" rating rests entirely on the solved matrix (Finding 1) and on
perfect information *combined with* a trivial matrix (Finding 3's kill
condition). That sharpening independently confirms the audit's §6 ordering:
fix the matrix first; everything else is a complement.

**Targets:**

- **Finding 1 [Matrix, Critical]** — every unit pair is an invincible
  doom-stack; root cause is the 4-node structure itself.
- **Finding 2 [Matrix, High]** — sparse, tie-heavy core; neutral matchups
  let players opt out of the mind-game; tiny option pool.
- **Finding 3 [Information, High]** — perfect information under sequential
  turns degrades prediction into calculation.
- **Engines:** Positional planning (broken), Pattern mastery
  (at risk → broken), Challenge (at risk), Self-determination (threatened).
- Finding 4 (Medium) is a process discipline — applied throughout: every
  matchup claim below is tested against the pure chart before any spatial
  story is told. Finding 5 (Low/Medium) is a load constraint — built into
  P1's design rather than targeted separately.

**Directive:** user asked to *"go bigger, pivots allowed — redesign the
hex-crawler combat loop."* Parsed: **boldness** — "go bigger" authorizes
pillar-bends outside the wildcard slot and up to two wildcards; "pivots
allowed" removes the identity cap entirely (identity checks still reported
per proposal). No count requested → 3 proposals. **Direction** — silent →
top live findings (1, 2, 3) + the weakest engines (all four; Positional
planning is the defining one).

**Cognitive-load posture:** 4 nodes / 6 matchups now, comfortably low;
declared ceiling ≈ 7 nodes / 21 matchups. Any expansion must arrive with a
load answer (Finding 5).

## 2. Portfolio

| # | Proposal | Move (design-moves entry) | Targets | Boldness |
|---|----------|---------------------------|---------|----------|
| P1 | **The War Wheel** — wired 7-node 2-Paradox battle chart (QR7), army-level verified | 2-Paradox expansion + Densify neutrals + Add node (Family 1) | Findings 1, 2 (+5 mitigation); Positional planning, Pattern mastery, Self-determination, Challenge | identity-preserving (load pillar bent, directive-authorized) |
| P2 | **Sealed Orders** — simultaneous written orders, WeGo resolution | Resolution-timing bend (Family 4), composed with Information structure (hidden *intent*) | Finding 3; Prediction loop (true), Positional planning | **[Wildcard — identity-stretching]** |
| P3 | **The Three Banners** — multi-objective victory; the battle becomes a Blotto game | Amplify: Positional planning (*objective placement that forces rotations*), scaled to a win-condition pivot (no catalog entry for that — extension declared) | Finding 1 (consequence layer), Finding 3 (partial); Positional planning, Challenge | pivot (directive-authorized) |

Coverage: Finding 1 ← P1 (root) + P3 (consequence) · Finding 2 ← P1 ·
Finding 3 ← P2 (root) + P3 (partial) · all four engines ← §3 tables.
The three proposals are modular and designed to stack (§4).

## 3. Proposals

### P1 — The War Wheel (7-node 2-Paradox battle chart)

**Mechanic spec**

*The chart.* Seven archetypes seated on a wheel, clockwise:

> **Pikemen → Cavalry → Archers → Siege → Fliers → Mages → Infantry → (Pikemen…)**

One rule wires all 21 edges: **each unit beats the units 1, 2, and 4 seats
clockwise from it** (and loses to the other three). This is the
quadratic-residue (Paley) tournament on 7 nodes — the proven-minimal
2-Paradox graph (interaction-structure §2.5, Query 4). The legacy quartet
sits on four consecutive seats (Infantry, Pikemen, Cavalry, Archers), so
**all four original counter edges survive unchanged**: Infantry > Pikemen >
Cavalry > Archers(Ranged) > Infantry.

Full chart (row vs column):

|  | Pikemen | Cavalry | Archers | Siege | Fliers | Mages | Infantry |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Pikemen** | — | **W** | **W** | L | **W** | L | L |
| **Cavalry** | L | — | **W** | **W** | L | **W** | L |
| **Archers** | L | L | — | **W** | **W** | L | **W** |
| **Siege** | **W** | L | L | — | **W** | **W** | L |
| **Fliers** | L | **W** | L | L | — | **W** | **W** |
| **Mages** | **W** | L | **W** | L | L | — | **W** |
| **Infantry** | **W** | **W** | L | **W** | L | L | — |

Role stories (each unit's row compresses to one line — this, plus the wheel
rule, is the load answer):

| Unit | Beats | Story |
|---|---|---|
| Pikemen | Cavalry · Archers · Fliers | a hedge of points — skewers charges, grinds into bow lines, bristles skyward |
| Cavalry | Archers · Siege · Mages | speed kills everything that stands and shoots |
| Archers | Siege · Fliers · Infantry | arrows pick off crews, wings, and shield-walls |
| Siege | Fliers · Mages · Pikemen | a stone doesn't care how high, how arcane, or how long your spear is |
| Fliers | Cavalry · Mages · Infantry | swoops over shields, panics horses, dives the casting circle |
| Mages | Infantry · Pikemen · Archers | fire annihilates massed foot — every line that stands still burns |
| Infantry | Pikemen · Cavalry · Siege | the drilled square — breaks pikes, repels the charge, storms the engines |

The two former neutrals are densified as **Infantry beats Cavalry** (the
square repels the charge) and **Pikemen beat Archers** (armored pike blocks
grind through the arrow-storm). These orientations are a design *choice*,
not a mathematical necessity: enumerating all embeddings of the legacy
4-cycle into the Paley tournament yields **84 embeddings covering all four
orientation combinations** of the two former-neutral edges — so if
playtesting wants Cavalry > Infantry or Archers > Pikemen instead, a
re-seating exists, but it reassigns the three new units' edges too and
**must be re-run through the script** before shipping.

*Spatial role hooks* (qualitative — the stat layer stays out of scope, as
in the audit): Siege attacks at 2-hex range and moves slowest; Fliers move
fastest and may pass over occupied hexes; Mages' attack splashes one hex
adjacent to the target; the legacy four keep their current movement
profiles. These give the three new archetypes distinct *grid* identities so
the spatial layer (pillar 2) has more texture to work with — they do not
alter any chart outcome.

*Armies.* Both sides field any 4 distinct archetypes of the 7 (the current
loop's army size, kept). Composition space grows from 1 forced army (the
quartet) to **C(7,4) = 35 armies**.

**Rationale**

- Targets **Finding 1** at its root, the way the audit's Lever A gestured
  but did not deliver: this is the wired chart, script-certified 2-Paradox
  — no pair of units is safe from a single counter — plus an **army-level
  guarantee the audit never touched**: on the pair-vs-pair chart, *no
  4-unit army (pair of pairs) is safe from a 2-unit counter-detachment*
  (verified below).
- Targets **Finding 2** by composition with **Densify neutrals**: the chart
  is a full tournament — zero non-mirror neutral matchups — so there is no
  engagement a player can lock into to opt out of the counter-web. Decisive
  engagement rate under uniform play rises **50% → 85.7%**.
- Beyond the audit (standing rule 3): Lever A named the node count, three
  example labels, and an instruction to verify. Delivered here and not in
  the audit: the actual QR7 wiring with the legacy quartet embedded on
  consecutive seats; the one-rule mnemonic + role-story load design (a
  different mitigation than Lever D's act-subsetting, which remains
  compatible but is not claimed); the 84-embedding design-space analysis;
  the pair-level (army) verification; the neutral-densification composition
  (the audit discussed filling neutrals only as an *insufficient
  alternative* to 7 nodes, not as a composed component); spatial role hooks
  for the three new archetypes.
- Moves used (design-moves, Family 1): **2-Paradox expansion** composed with
  **Densify neutrals** and **Add node**.

**Theory-test evidence**

Before (audit chart, re-run) — key lines, verbatim:

```
Mode: binary | Nodes: 4 (Infantry, Cavalry, Ranged, Pikemen)
Tournament: no (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Infantry -> Pikemen -> Cavalry -> Ranged -> Infantry
3-cycles: 0
Dominated nodes: none
6 unbeatable subset(s) of size 2 — 2-Paradox property does NOT hold:
[…all 6 pairs…]
```

After (War Wheel), verbatim — every pass bar met (`Dominated nodes: none`;
the exact 2-Paradox line; tournament confirmed for the densification test):

```
Mode: binary | Nodes: 7 (Pikemen, Cavalry, Archers, Siege, Fliers, Mages, Infantry)

== STRUCTURE ==
Tournament: yes (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Pikemen -> Cavalry -> Archers -> Siege -> Pikemen
3-cycles: 14

== DOMINATED NODES ==
Dominated nodes: none

== DOOM-STACKS (unbeatable subsets) ==
size 2: none — the 2-Paradox property holds.

== VIABILITY (eigenvector centrality, steady-state heuristic) ==
  Archers: 0.1429
  Cavalry: 0.1429
  Fliers: 0.1429
  Infantry: 0.1429
  Mages: 0.1429
  Pikemen: 0.1429
  Siege: 0.1429
```

| Metric | Base (before) | War Wheel (after) | Delta |
|---|---|---|---|
| Dominated nodes | none | none | **pass bar met: no new dominated nodes** |
| Size-2 doom-stacks | 6 (every pair) | **none — 2-Paradox holds** | Finding 1 resolved at the root |
| Tournament / intransitive | no / yes (0 3-cycles) | **yes** / yes (**14** 3-cycles) | Finding 2 resolved; 14× counter-play texture |
| Decisive engagements (uniform play) | 50.0% | 85.7% | opt-out neutrals gone |
| Viability | uniform 0.2500 | uniform 0.1429 | symmetry pillar preserved exactly |
| Armies (4 distinct units) | 1 | 35 | autonomy has something to choose |

*Army-level verification* (the fielded army is 4 units = a pair of pairs, so
the pair-chart's size-2 doom-stack scan asks precisely: **is any full army
unanswerable by a 2-unit task force?**). Pair-vs-pair charts: 21 pair-nodes
(after) / 6 (before); entry = sum of the 4 cross-matchup outcomes
(same-unit cross-matchups = 0 — the model proven on the RPS redesign's Twin
format).

Before — the pathology recurses upward, verbatim key lines:

```
Mode: weighted | Nodes: 6 (Infantry+Cavalry, Infantry+Ranged, […])
Tournament: no (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Infantry+Ranged -> Infantry+Pikemen -> Cavalry+Pikemen -> Cavalry+Ranged -> Infantry+Ranged
3-cycles: 0
Dominated nodes: none
15 unbeatable subset(s) of size 2 — 2-Paradox property does NOT hold:
[…all C(6,2) = 15 pair-of-pair subsets — i.e. every possible 4-unit army…]
```

Two new base-game facts fall out of that run (sharpening Findings 1–2
beyond the audit): **every 4-unit army is unanswerable** by any single
2-unit detachment, and composition is strategically void — only 22.2% of
ordered pair matchups are decisive at all, and **every disjoint
pair-vs-pair matchup sums to exactly 0** (any two armies that share no
unit type are a dead draw on composition; only the spatial layer decides
anything).

After — verbatim key lines:

```
Mode: weighted | Nodes: 21 (Pikemen+Cavalry, Pikemen+Archers, […], Mages+Infantry)
Tournament: no (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Pikemen+Cavalry -> Pikemen+Archers -> Pikemen+Fliers -> Pikemen+Cavalry
3-cycles: 147

== DOMINATED NODES ==
Dominated nodes: none

== DOOM-STACKS (unbeatable subsets) ==
size 2: none — the 2-Paradox property holds.

== VIABILITY ==
  (all 21 pairs): 0.0476
```

| Army-level metric | Base | War Wheel | Delta |
|---|---|---|---|
| Unbeatable 4-unit armies (pair-of-pairs) | **15 — all of them** | **none** | every army admits a 2-unit answer |
| Dominated pairs | none | none | pass bar met at pair level too |
| Decisive pair matchups (ordered, incl. mirrors) | 22.2% | 76.2% | composition play goes live |
| Pair viability | uniform 1/6 | uniform 1/21 | no privileged detachment |

**Engine deltas**

| Engine | Sustains added | Kills removed / added | Health |
|---|---|---|---|
| Positional planning | a matrix deep enough that position matters (design-moves amplifier precondition — now met); 14 3-cycles of local counter-texture; new grid roles (range-2, overflight, splash) | removed: "matrix so shallow the board is solvable regardless of position" (fun-engines kill) | broken → **healthy** (conditional on the stat layer, §6) |
| Pattern mastery | 21 edges behind one generative rule + 7 role stories; 35-army building metagame; army-level counter-web (147 3-cycles) | removed: solved patterns (no static solve exists — script); added: option bloat risk at the 7-node cap (mitigated, flagged) | at risk → broken → **healthy** |
| Challenge | no dominant composition to find (script); every army beatable | removed: the dominant-strategy collapse (audit §4 kill) | at risk → **healthy** |
| Self-determination | 35 armies, enforced-viable: uniform 1/7 unit and 1/21 pair centrality (design-moves "Amplify: Self-determination" — near-uniform = healthy autonomy, by the script) | removed: "one true build" | threatened → **healthy** |

Cross-engine damage line: **the low-load pillar takes the hit** — 6 → 21
matchups is exactly the strain Finding 5 predicted; the wheel rule, role
stories, and card-affordance UI (each unit card fans out its three prey)
are the mitigation, and act-based subsetting (audit Lever D) remains
available as onboarding. Flow is the second exposure: seven identities on
day one can spike the novice curve.

**Costs**

- Cognitive load: matchup pool **6 → 21** (the declared ceiling; Query 1:
  pass **at cap**, with the generative rule carrying the memorization —
  players learn 1 rule + 7 stories, not 21 edges). Composition pool 1 → 35
  armies (a strategic-layer choice, not per-turn parsing).
- Could damage: Flow (novice ramp); session pacing if players stop to
  consult the wheel (UI affordance is load-bearing).
- Implementation scope: **M** — three unit archetypes with role hooks,
  chart data, wheel UI, teaching material.

**Identity check**

| Pillar | Verdict | Note |
|---|---|---|
| Sequential resolution | preserved | untouched |
| Spatial hex maneuver | preserved (enriched) | three new grid roles; no spatial rule removed |
| Intransitive counter-web core | preserved (deepened) | legacy 4-cycle embedded verbatim; script: intransitive, 14 cycles |
| Symmetric roster | preserved | same 7 archetypes both sides; uniform centrality |
| Low cognitive load | **bent** (directive-authorized) | 6 → 21 at the declared ceiling; mitigations above; Finding 5 honored, not dodged |

### P2 — Sealed Orders (simultaneous WeGo turns) **[Wildcard — identity-stretching]**

**Mechanic spec**

- **Order phase (simultaneous, secret):** each round, both players write
  orders for *all* of their units at once — a movement path (up to that
  unit's allowance) and nothing else; engagement is automatic on contact.
  Orders are hidden until both sides commit. Army positions and
  compositions remain **fully public** — nothing about board *state* is
  hidden, only *intent*.
- **Resolution phase (simultaneous, deterministic):** all units advance
  along their paths one hex per step, all at the same time.
  - Two units ordered into the same hex on the same step: both stop on the
    hexes they came from (**bump rule**).
  - Two units ordered through each other (swap): both stop adjacent —
    swapping through an enemy is impossible.
  - A unit that becomes adjacent to an enemy unit at any step **halts**
    (contact); remaining path is discarded.
- **Combat phase:** every contacted enemy-adjacent unit fights; outcomes
  resolve by the interaction chart exactly as the current loop resolves
  them (attrition model inherited unchanged). No order modifies any
  matchup — **the effective chart is the declared chart**.
- Table talk during the order phase is explicitly legal (free bluff
  bandwidth; no rules needed).

Works standalone on the 4-node chart; designed to compose with P1's chart.

**Rationale**

- Targets **Finding 3 at its root**. The audit's own Lever B concession —
  "fog only delays the solve" — is the design-moves trigger for this exact
  move: *Resolution-timing bend — when the audit shows calculation has
  replaced prediction, and information moves alone are too weak* (Family 4).
  Sequential + perfect information devolves into deterministic reaction
  (interaction-structure §1.2); hiding *state* (fog) postpones the
  computation, but hiding *intent* via simultaneous commitment removes the
  premise — there is no opponent-move to compute a best response to,
  because both maneuver plans resolve together. Prediction is restored as
  a structural property, not an information patch.
- This goes beyond, not through, audit Levers B and C (standing rule 3):
  no state is hidden (≠ fog), and no action budget changes (≠ action
  economy). It installs the Prediction loop's missing pillar
  (simultaneity — interaction-structure §1.2, pillar 1) in the one place
  the genre note says a sequential game may legitimately acquire it: by
  *becoming* simultaneous at the maneuver layer.
- Iterated rounds of committed orders accumulate behavioral data —
  "what is this actor's frequency bias" now applies to flank preferences
  and screen placements (interaction-structure §2.1).
- Moves used: **Resolution-timing bend** (Family 4) composed with
  **Information structure** (systemic-levers — hidden information as the
  sequential-play substitute for simultaneity, here applied to intent) and
  free **bluff bandwidth**.

**Theory-test evidence**

Layer/wildcard move — the interaction chart is untouched, so the P1
(or base) runs apply verbatim; no matchup values change. The Family 4 test
hook ("if the change alters effective matchups — initiative removal —
re-run the script on the effective chart") resolves as: **no re-run
needed, and the declared chart becomes *more* faithful**. Under sequential
IGO-UGO, the acting player chooses which engagements happen, so realized
matchup frequencies carry a mover bias the declared chart doesn't encode;
under WeGo, engagements arise from two committed plans meeting, which is
exactly the symmetric row-vs-column semantics the chart declares. Theory
anchors, mapped per standing rule 4:

- interaction-structure §1.2 (pillar 1): "Actions must resolve
  concurrently. If turns are sequential without hidden information, the
  system devolves into deterministic reaction" — P2 makes maneuver
  resolution concurrent; Finding 3's mechanism is removed, not masked.
- interaction-structure §3.2: simultaneous execution rewards psychological
  profiling; sequential+spatial rewards planning trees — P2 deliberately
  moves the game one notch toward profiling *while keeping the planning
  tree* (paths are multi-turn plans).
- systemic-levers, Information structure: hidden information restores a
  prediction burden in sequential games; its failure mode ("so much is
  hidden that decisions feel like coin flips") is structurally capped here
  because only one round of intent is ever hidden — all state stays public.

**Engine deltas**

| Engine | Sustains added | Kills removed / added | Health |
|---|---|---|---|
| Prediction loop (true, simultaneous) | its structural pillar: simultaneity of commitment; behavioral reads compound across rounds (§2.1); free bluff bandwidth | removed: "broken simultaneity / turn order leaks intent" | N/A by genre → **present & healthy** (this proposal *changes the genre-fit*) |
| Positional planning | committed multi-turn plans raise the stakes of every read; screens/interceptions become predictions, not reactions | added: novices may experience committed movement as loss of control | broken → **healthy when composed with P1** (alone, it still sits on a solved 4-node chart — see conflicts, §4) |
| Pattern mastery | opponent habit modeling (flank bias, screen habits) — a second mastery channel | — | at risk → improved |
| Challenge | reads and feints become skill-expressive | **added: the pure-calculation audience loses its solvable tree** — the deliberate trade | at risk → healthy for the target audience; changed audience |
| Fellowship | simultaneous reveals are a table moment | — | minor gain |

Cross-engine damage line: **Challenge (calculation flavor) and Flow** —
players who loved the chess-like solvability lose it by design, and
simultaneous resolution can be chaotic to read (bump-rule pileups); the
resolution animation/log is load-bearing UI, and the bump rules must stay
tiny or Flow pays.

**Costs**

- Cognitive load: matchup pool unchanged (Query 1: pass). Planning breadth
  rises — all units are ordered per round instead of one activation at a
  time; state to track is unchanged (all public).
- Could damage: Flow (resolution readability); onboarding (WeGo is
  unfamiliar to the HoMM audience).
- Implementation scope: **L** — order UI, simultaneous resolver, replay/log
  presentation; the deepest engineering item in this portfolio.

**Identity check**

| Pillar | Verdict | Note |
|---|---|---|
| Sequential resolution | **broken** | the wildcard: rounds are simultaneous WeGo — this is the stretched pillar |
| Spatial hex maneuver | preserved (intensified) | maneuver is now the entire read |
| Intransitive counter-web core | preserved | chart untouched; effective = declared |
| Symmetric roster | preserved | identical order rules both sides |
| Low cognitive load | preserved (strained) | nothing new to memorize; per-round planning breadth rises |

### P3 — The Three Banners (multi-objective victory pivot)

**Mechanic spec**

- **Board:** three banner hexes, fixed and symmetric — one per board third
  (left / center / right), equidistant from both deployment edges.
- **Deployment:** unchanged armies (4 units in the base game; 4-of-7 under
  P1), deployed on home edges after seeing the banner positions (banners
  are terrain, not hidden).
- **Holding a banner:** a banner is held by the side whose unit stands on
  it. If no unit stands on it, it stays with the last holder (plant the
  flag); at battle start, banners are unheld.
- **Victory:** the battle ends immediately if an army is destroyed
  (annihilation still wins — armies still matter). Otherwise, at the end
  of round 8, the side holding more banners wins. If banner counts tie,
  play sudden-death rounds until they differ at a round's end.
- No other rule changes: movement, combat, and attrition resolve exactly
  as the current loop does (or as P1/P2 define when composed).

The strategic consequence, not a rule: with three separated scoring sites
and one army, **every turn is an allocation decision** — how many units
press which banner. That allocation game is the theory-tested object below.

**Rationale**

- Targets **Finding 1 at the consequence layer** — honestly framed per the
  audit's own warning (spatial/systemic levers *mask* a solved matrix
  rather than solving it; §6 ordering note): P3 does not repair the chart,
  and is not claimed to. What it does is make the doom-stack **pay for its
  invincibility in presence**: an unbeatable 2-stack can hold one banner,
  not three. The audit's Finding-1 sentence — "the interaction core being
  solved on turn one" — stops being the game's death because the *war* is
  decided at a layer the stack cannot cover. The verification below shows
  the all-in allocation (the literal doom-stack posture, all units on one
  front) is **dominated** — the script's word — by split allocations: in
  the base game the stack was unanswerable; under Three Banners, stacking
  is *provably never a better pick*.
- Targets **Finding 3 partially**: allocation is a simultaneous-in-effect
  guessing game even under perfect information and sequential turns —
  redeploying between distant banners costs multiple turns, so commitment
  to a front is de facto irreversible when made, and the intransitive
  allocation chart below means there is no allocation to calculate your
  way to. Weaker than P2's root fix; real nonetheless.
- Beyond the audit (standing rule 3): no §6 lever touches objectives or
  win conditions. P3 also *supersedes Lever C's intent* — "the right
  counter-unit can't always reach the target hex in time" — and delivers it
  through commitment geometry (the counter is three turns away by choice)
  rather than movement-point scarcity (a knob the audit itself called
  fiddly-risk).
- Moves used: **Amplify: Positional planning** — *objective placement that
  forces rotations* (design-moves Family 3, quoted) — scaled past an
  amplifier into a win-condition pivot; the catalog has no win-condition
  entry, so this extension is declared rather than cited (attribution
  honesty). The allocation model is the **Colonel Blotto game** (Borel,
  1921) — the canonical simultaneous-allocation structure; its known
  property (no pure equilibrium; intransitive best-responses) is what the
  script run certifies for this instance.

**Theory-test evidence**

Synthetic allocation chart, following the pair-vs-pair verification
pattern: nodes = the 15 ordered splits of 4 units across 3 lanes
(left-center-right); a lane is won by strict local superiority; matchup
outcome = sign(lanes won − lanes lost). This count model is deliberately
**matrix-blind** (units as interchangeable bodies) — the worst case for
allocation depth; the real game only adds counterplay on top (a lane's
2-vs-1 is not an automatic win once unit types exist — under P1, lane
fights *are* the verified pair-vs-pair chart). Verbatim key lines:

```
Mode: binary | Nodes: 15 (0-0-4, 0-1-3, 0-2-2, 0-3-1, 0-4-0, 1-0-3, 1-1-2, 1-2-1, 1-3-0, 2-0-2, 2-1-1, 2-2-0, 3-0-1, 3-1-0, 4-0-0)

== STRUCTURE ==
Tournament: no (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: 0-1-3 -> 2-0-2 -> 0-3-1 -> 2-2-0 -> 0-1-3
3-cycles: 14

== DOMINATED NODES ==
0-0-4 is DOMINATED by 0-1-3 (never a better pick).
0-0-4 is DOMINATED by 1-0-3 (never a better pick).
0-0-4 is DOMINATED by 1-1-2 (never a better pick).
0-4-0 is DOMINATED by 0-3-1 (never a better pick).
0-4-0 is DOMINATED by 1-2-1 (never a better pick).
0-4-0 is DOMINATED by 1-3-0 (never a better pick).
4-0-0 is DOMINATED by 2-1-1 (never a better pick).
4-0-0 is DOMINATED by 3-0-1 (never a better pick).
4-0-0 is DOMINATED by 3-1-0 (never a better pick).

== VIABILITY (eigenvector centrality, steady-state heuristic) ==
  1-1-2: 0.0820
  1-2-1: 0.0820
  2-1-1: 0.0820
  0-2-2: 0.0784
  2-0-2: 0.0784
  2-2-0: 0.0784
  0-1-3: 0.0672
  0-3-1: 0.0672
  1-0-3: 0.0672
  1-3-0: 0.0672
  3-0-1: 0.0672
  3-1-0: 0.0672
  0-0-4: 0.0386
  0-4-0: 0.0386
  4-0-0: 0.0386
```

Reading, against the pass bars:

- **The three all-in stacks are the only dominated nodes — by design.**
  This is the proposal's entire point rendered in the script's own
  vocabulary: the doom-stack posture is *never a better pick*. The
  universal pass bar ("no new dominated nodes") applies to charts players
  pick units from; the **unit chart is untouched — zero dominated units
  introduced**. Dominance *inside the allocation layer* is the intended
  deterrent, disclosed exactly as the audit skill's precedent discloses
  deliberately-broken teaching subsets: verified, not asserted. The live
  allocation pool self-prunes 15 → 12.
- **INTRANSITIVE, 14 3-cycles** at the allocation layer: there is no
  allocation to solve for — best responses cycle (the Blotto property),
  which is what makes allocation a *prediction* under perfect information
  (the Finding 3 contribution).
- 57 unbeatable *pairs of allocations* exist; a pair here is two
  alternative plans, not two things fielded together — an unbeatable pair
  means "no single plan answers both," i.e. **mixing between those two
  plans has no pure counter**, which is the mechanism that forces mixed
  (unpredictable) play. In an allocation chart this is the healthy
  outcome, not the doom-stack pathology (whose home domain is co-fielded
  subsets); reported for completeness.
- 57.1% of distinct allocation matchups are neutral (mostly
  permutation-mirrors): allocation neutrality hands resolution *down* to
  the tactical layer in each lane — allocation decides where the fights
  are, the matrix decides the fights. The layers divide labor rather than
  double-resolve.
- Compound check (P1+P3 with larger armies): the 6-unit, 3-lane chart
  (28 allocations) reproduces the structure — dominated allocations:
  exactly `(0,0,6), (0,6,0), (6,0,0)` — the anti-stacking theorem is not
  an artifact of the 4-unit count.

**Engine deltas**

| Engine | Sustains added | Kills removed / added | Health |
|---|---|---|---|
| Positional planning | objective placement forces rotations (the amplifier, verbatim); consequential space — banners make position *the* scoreboard; redeployment tempo becomes a resource without new rules | removed: "positioning with no real consequence"; added: none | broken → **healthy when composed with P1**; alone: much improved but sitting on a solved unit chart (§4) |
| Challenge | comeback structure (concede a lane, win the other two); anti-snowball geometry — a winning stack is a stack not scoring elsewhere | removed: dominant-strategy stacking (script: dominated); added: draw-adjacent standoffs (sudden death mitigates) | at risk → **healthy** |
| Prediction loop | allocation mind-game with no pure answer (script: intransitive) — prediction under perfect information | — | absent → present (lighter than P2's) |
| Pattern mastery | allocation shapes as a learnable vocabulary (2-1-1 pressure vs 3-1-0 punch) | — | improved |
| Self-determination | plans differentiate (rusher / split-presser / counter-puncher styles) | — | improved |

Cross-engine damage line: **the annihilation fantasy** — total-battle
catharsis (Sensation/Fantasy, MDA) dilutes when battles end on banners
with armies still standing; the round-8 horizon can read as arbitrary
(Flow) — annihilation-still-wins and sudden death are the mitigations.

**Costs**

- Cognitive load: unit matchup pool unchanged; allocation adds a plan-level
  vocabulary of 15 splits (self-pruning to 12; three interchangeable-shape
  classes to actually learn). Query 1: pass — allocation is a per-battle
  posture, not per-engagement parsing.
- Could damage: Sensation/Fantasy and Flow (above); risk of banner-camping
  degeneracy if attrition is toothless (stat-layer dependent, §6).
- Implementation scope: **M** — banner terrain, hold-tracking, victory
  logic, sudden death; no new unit content.

**Identity check**

| Pillar | Verdict | Note |
|---|---|---|
| Sequential resolution | preserved | turn structure untouched |
| Spatial hex maneuver | preserved (promoted) | space becomes the win condition, not just the route to matchups |
| Intransitive counter-web core | preserved | chart untouched; a second intransitive web (allocation) layered above it, script-verified |
| Symmetric roster | preserved | symmetric banners, identical victory terms |
| Low cognitive load | preserved (lightly bent) | +1 plan-level vocabulary; no new matchups |
| *(implicit frame: battle-to-annihilation)* | **pivoted** (directive-authorized) | victory redefined from kill-the-army to hold-the-field — the pivot the directive licenses |

## 4. Recommendation & sequencing

**Pursue P1 first.** It is the only proposal that removes the root
pathology (the audit's own ordering note: everything else *masks* a solved
matrix), it meets every scripted pass bar including the exact 2-Paradox
line at both the unit and the army level, it repairs four engines in one
stroke, and it is the smallest scope of the three (M). Nothing else in
this portfolio reaches its potential until the chart underneath it is
unsolvable.

**Then P3.** Medium scope, zero new unit content, and it compounds
multiplicatively with P1: banners force armies to split, and under P1
*every* split detachment remains answerable (pair-level 2-Paradox), so
lane fights are live matchup questions instead of count checks — the
blotto-6 run confirms the allocation structure survives the larger armies
P1 enables. P1+P3 is the identity-respecting "operational depth" build:
still sequential, still HoMM-shaped, dramatically harder to solve.

**P2 last, as the boldness gate.** It is the largest engineering lift (L),
the deepest identity change (the wildcard), and the one whose audience
trade (calculation → reads) most needs a playtest verdict. With P1 in
place, Finding 3 already softens — fun-engines is explicit that perfect
information alone is not a kill when the planning tree is deep (chess) —
so P2 becomes a *transformation choice*, not a repair: adopt it if
playtests show the deterministic maneuver duel still feels solvable-flat
rather than deep.

**Compounds:** P1+P3 (recommended core build) · P1+P2 (the double-blind
tactics duel) · P1+P2+P3 (the full "Kriegsspiel edition" — committed
secret maneuver plans across three fronts on an unsolvable chart; the
portfolio's horizon build).

**Conflicts:**

- **P2 and P3 standalone (without P1) both under-deliver:** each layers
  prediction on top of a still-solved 4-node chart — fog-lever logic the
  audit already rejected applies equally to them; neither is a substitute
  for P1. Sequence, don't substitute.
- **P2 × P3 load-stacking:** simultaneous multi-unit order writing *and*
  three-front allocation in one round is the portfolio's cognitive
  worst case. Playtest-gate the triple build; introduce one layer at a
  time.
- No two proposals fight over the same engine: P1 feeds the matrix all
  engines eat from; P2 amplifies the read; P3 amplifies the map. The
  overlap (both P2 and P3 add prediction) is additive-with-diminishing-
  returns, not contradictory.

## 5. Re-audit handoff (Path-B spec) — The War Wheel

Self-contained rules; auditable cold.

**Players:** 2, symmetric. **Setting:** turn-based tactical battles on a
hex grid (the tactical layer of a strategy campaign; the campaign layer is
out of scope).

**Unit roster (7 archetypes, both sides):** Pikemen, Cavalry, Archers,
Siege, Fliers, Mages, Infantry.

**Interaction chart** (row vs column; W = row wins the engagement, L = row
loses; mirror matchups are even; no other neutral outcomes exist):

|  | Pikemen | Cavalry | Archers | Siege | Fliers | Mages | Infantry |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Pikemen** | — | W | W | L | W | L | L |
| **Cavalry** | L | — | W | W | L | W | L |
| **Archers** | L | L | — | W | W | L | W |
| **Siege** | W | L | L | — | W | W | L |
| **Fliers** | L | W | L | L | — | W | W |
| **Mages** | W | L | W | L | L | — | W |
| **Infantry** | W | W | L | W | L | L | — |

Generative form (equivalent to the table): seat the seven units on a wheel
in the order Pikemen, Cavalry, Archers, Siege, Fliers, Mages, Infantry;
each unit beats the units 1, 2, and 4 seats clockwise from it.

**Armies:** each player fields 4 units of distinct archetypes, chosen from
the 7 before deployment (35 possible armies).

**Spatial rules:** inherited from the base loop (hex movement, maneuvering
to force engagements). Role hooks for the three archetypes beyond the
legacy four: Siege attacks targets 2 hexes away without adjacency and has
the slowest movement; Fliers have the fastest movement and may pass over
occupied hexes (they end moves on empty hexes); Mages' attacks splash one
hex adjacent to the target. Numeric movement/attrition values are a
tuning layer, deliberately unspecified here as in the source design.

**Combat resolution:** when units engage, the chart decides the exchange
in the winner's favor; mirror engagements are even. Attrition and
army-break conditions are inherited from the base loop unchanged.

**Economy:** none at the tactical layer (no faucets/sinks introduced).

**Information structure:** fully open — both armies and all positions are
visible; turns are sequential as in the base loop.

**Victory:** destroy or break the opposing army (base-loop condition,
unchanged).

> To validate independently, run the game-analysis skill against this
> section in a fresh session, and compare its findings with the audit that
> seeded this redesign.

## 6. Assumptions & open questions

- **Ground truth:** the seed audit is taken as-is; its own caveat inherits —
  everything here is archetype-level, and a stat layer (HP/damage/speed
  numbers) could distort any chart conclusion. Every proposal keeps stats
  out of scope exactly as the audit did.
- **Directive interpretation:** "go bigger, pivots allowed" parsed as
  identity-cap-removed, ≤2 wildcards, default count (3), default direction
  (top findings + weakest engines). One wildcard (P2) plus one pivot (P3)
  were used; if "bigger" meant *more proposals* (the grammar allows 2–5),
  say so and the portfolio extends.
- **Engine-name refinement:** the audit's "Prediction loop (spatial
  variant)" is treated as fun-engines' Positional planning per the
  genre-fit note; the audit's substance (matrix-starved engine) is
  unaffected, but its "simultaneity is absent" clause is genre-N/A rather
  than a defect. P2 is therefore framed as a transformation, not a repair.
- **Pair-vs-pair model:** army-level verification sums the four
  cross-matchup outcomes (same-unit = 0), the model validated on the RPS
  redesign's Twin format. Real engagements are modulated by position,
  attrition state, and stats; the pair chart is the stat-free skeleton.
  Playtest measure: do 2-unit counter-detachments actually beat the armies
  the chart says they answer, at plausible stat values?
- **Count-Blotto abstraction (P3):** lanes resolve by strict unit-count
  superiority, deliberately matrix-blind. With typed units the lane fight
  is the pair-vs-pair chart (verified separately), which adds counterplay
  rather than removing any. The dominance of all-in allocations was
  re-verified at 6-unit armies (28-allocation chart, same result); any
  other army size or banner count must be re-run, not assumed.
- **P1 densified-edge orientation:** Infantry > Cavalry and
  Pikemen > Archers are choices; 84 legacy-cycle embeddings exist covering
  all four orientation combinations, so thematic re-preference is
  achievable — but any re-seating rewires the new units' edges and must be
  re-scripted before shipping. Playtest measure: do the two densified
  edges read as fair ("the square holds!") or as arbitrary?
- **P1 learnability at the cap:** 21 matchups behind one wheel rule + 7
  role stories. Playtest measures: time-to-fluency vs the 4-unit baseline;
  wheel-consult frequency per battle after three sessions; novice Flow
  (does day-one exposure to 7 identities spike churn, and does act-gating
  fix it?).
- **P2 resolution readability:** bump/contact rules are minimal on paper;
  simultaneous pileups may still confuse. Playtest measures: how often
  players are surprised by *their own* resolution; whether a step-replay
  log is sufficient; whether committed movement reads as thrilling or as
  lost control.
- **P2 audience trade:** the calculation-lover loses the solvable tree by
  design. Playtest measure: session-2 retention split by player type
  (puzzle-preference vs read-preference).
- **P3 degeneracy risks:** banner-camping (if attrition is toothless,
  standing on flags beats fighting) and horizon gaming (round-8 clock
  play). Mitigations on paper: annihilation-still-wins, sudden death.
  Playtest measures: fraction of battles decided by annihilation vs
  banners; fraction reaching sudden death; whether round 7–8 play warps
  into clock abuse.
- **P3 draw pressure:** 57.1% of distinct allocation matchups are neutral
  at the count level; the design bets lane-level matchup play (and P1's
  chart when composed) resolves them. Playtest measure: how often battles
  feel "pre-drawn" at deployment.
- **Composed builds:** P1+P3 is recommended sight-unseen; P1+P2 and the
  triple build are playtest-gated (load stacking, §4). No composed build
  was chart-verified beyond the blotto-6 run; compose-then-re-audit is the
  loop for anything further.

---

*Method: game-redesign skill over the 2026-07-08 audit. Charts generated
and verified via `game-analysis/scripts/matrix_analysis.py --max-stack 2`
on five inputs (base, War Wheel, both pair-vs-pair charts, 15-node
allocation chart; plus a 28-node compound check). All script output quoted
verbatim with elisions marked. Framework claims attributed inline to
interaction-structure.md, fun-engines.md, systemic-levers.md, the
game-redesign design-moves catalog, MDA (Hunicke, LeBlanc & Zubek 2004),
Koster (2004), Ryan & Deci, and Borel (1921) for Colonel Blotto. This
document is theory-consistent, not play-tested.*
