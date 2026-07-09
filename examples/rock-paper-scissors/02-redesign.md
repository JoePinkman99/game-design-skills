# Rock Paper Scissors — Redesign Proposals

**Status: theory-consistent, not play-tested.**
Seeded by [rock-paper-scissors-analysis.md](rock-paper-scissors-analysis.md)
(Path A audit, 2026-07-07). Charts verified with the game-analysis skill's
`matrix_analysis.py`; script output quoted verbatim.

## 1. Design brief (echo)

**Identity pillars** (audit §2 + §4):

1. **Simultaneous, zero-reactivity throw** — both commit at once
   (interaction-structure §1.2, pillar 1).
2. **Balanced intransitive counter-cycle** — no dominant option; the
   1-Paradox core (audit §2 genre framing).
3. **Small option pool / low cognitive load** — audit's own ceiling: ≤7 nodes
   (interaction-structure §1.2 pillar 3, Query 1).
4. **Bare-hands Fellowship ritual** — countdown, face-to-face, zero equipment;
   the fair-decision-tool niche (audit §4, Fellowship: healthy).
5. **Player symmetry / fairness** — both sides face identical terms (audit §2).

**Targets** (audit §5 + §4):

- **#1 [Information] Single-shot collapse to pure chance** — top severity.
- **#3 [Systemic] Shallow ceiling + 33% tie rate.**
- **#2 [Matrix] 2-Paradox failure** — mechanically inert in base RPS; a live
  target only if a proposal adds multi-node fielding (audit's own condition).
- **Weakest engine: Pattern mastery — at risk** (shallow ceiling). Prediction
  loop is "healthy but conditional" — the conditionality *is* finding #1.

**Directive:** user asked to "propose redesigns … based on the audit" — silent
on both axes. Parsed as **default boldness** (2 identity-preserving + 1
wildcard) and **default direction** (top live findings + weakest engine).

**Cognitive-load posture:** base pool = 3 options; audit blesses ≤7 nodes and
warns that naive roster scaling kills the prediction loop (Query 1).

## 2. Portfolio

| # | Proposal | Move (design-moves entry) | Targets | Boldness |
|---|----------|---------------------------|---------|----------|
| P1 | **Sharpened Throws** — weighted win values + tie pot | Amplify: Prediction loop (*mixed-value outcomes* + *iterated stakes*) | Findings #1, #3; Pattern mastery | identity-preserving |
| P2 | **The Well Returns** — 7-node 2-Paradox chart, Solo + Twin formats, act-based onboarding | 2-Paradox expansion + Subset rotation (acts) + fielding layer | Findings #2, #3; Pattern mastery | identity-preserving (Twin tier strains pillar 3 — gated, flagged) |
| P3 | **Throwdown** — commit → bet → reveal, chip economy | Wildcard: resolution-timing + information bend, composed with Bluff bandwidth + Economy sink (systemic-levers) | Findings #1, #3; Prediction loop, Pattern mastery | **[Wildcard — identity-stretching]** |

Coverage: #1 ← P1+P3 · #2 ← P2 · #3 ← all · Pattern mastery ← all.

## 3. Proposals

### P1 — Sharpened Throws (weighted wins + tie pot)

**Mechanic spec**

- Who-beats-whom is unchanged. Scoring changes: **win with Rock = 1 point,
  win with Paper = 2, win with Scissors = 3.**
- **Tie pot:** each tied round adds 1 point to a pot; the next decisive
  round's winner scores throw value **+ pot**; pot resets to 0.
- **Match:** first to 7 points.
- Value assignment is unique up to relabeling; the load-bearing structure is
  *cheap beats expensive*: Rock (1) beats Scissors (3), Paper (2) beats
  Rock (1), Scissors (3) beats Paper (2). Betting on the big prize is
  answered by the cheapest throw.

**Rationale**

- Targets **finding #1**: in base RPS the lazy strategy (uniform 1/3) is
  mathematically unexploitable, so one-shot skill cannot exist. Weighted wins
  destroy that safety: the optimal mix becomes non-obvious (Rock 1/2,
  Paper 1/6, Scissors 1/3 — verified below), and *every* naive strategy
  becomes exploitable. Skill floor and ceiling separate immediately.
- Targets **finding #3**: ties stop being dead — they charge the pot — and
  mastery gains a ladder (learn the mix → estimate opponent's deviation →
  exploit it → re-hide). The pot continuously *moves* the equilibrium (table
  below), so reads never stabilize.
- Engines: **Prediction loop** and **Pattern mastery** (audit §4). Moves used
  (design-moves, Family 3 "Amplify: Prediction loop"): *mixed-value outcomes —
  some wins worth more, skews frequency bias and deepens reads* — composed
  with *iterated stakes (carry-over between rounds so reads compound)*.
- Beyond the audit (standing rule 3): audit §6.1 proposed plain best-of-N
  iteration; this adds value asymmetry and carry-over stakes, neither named
  in the audit.

**Theory-test evidence**

Before/after script runs (encoding: `matrix[i][j]` = points row scores off
column; auto-detected weighted mode). After-run, verbatim:

```
Mode: weighted | Nodes: 3 (Rock, Paper, Scissors)

== STRUCTURE ==
Tournament: yes (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Rock -> Scissors -> Paper -> Rock
3-cycles: 1

== DOMINATED NODES ==
Dominated nodes: none

== DOOM-STACKS (unbeatable subsets) ==
3 unbeatable subset(s) of size 2 — 2-Paradox property does NOT hold:
  ('Rock', 'Paper')
  ('Rock', 'Scissors')
  ('Paper', 'Scissors')

== VIABILITY (eigenvector centrality, steady-state heuristic) ==
  Scissors: 0.4626
  Paper: 0.2818
  Rock: 0.2556
```

| Metric | Base (before) | Sharpened (after) | Delta |
|---|---|---|---|
| Tournament / intransitive | yes / yes (1 cycle) | yes / yes (1 cycle) | structure preserved |
| Dominated nodes | none | none | **pass bar met: no new dominated nodes** |
| Size-2 doom-stacks | 3 (all pairs) | 3 (identical) | unchanged — still inert (single throw fielded) |
| Viability | uniform 0.3333 ×3 | 0.4626 / 0.2818 / 0.2556 | asymmetric incentives achieved (design goal) |

Centrality caveat: weighted-mode centrality reads *raw scoring power*
(Scissors carries the 3-point prize). Strategic ground truth is the Nash
mix, hand-derived and machine-checked (supplementary, from the zero-sum
form `R:[0,−2,1] P:[2,0,−3] S:[−1,3,0]`):

- Claimed mix (R, P, S) = (1/2, 1/6, 1/3) → indifference EVs = (0, 0, 0) ✓.
- Vs a **uniform** opponent, pure Scissors earns **+2/3 per round** — the
  base game's safe strategy is now punishable (the finding-#1 mechanism).
- Tie probability if both play Nash: **7/18 ≈ 38.9%** (up from 33.3%) —
  honest cost, mitigated because ties now charge the pot.
- Pot interpolation (chip-scored model): Nash mix at pot v is
  (3+v, 1+v, 2+v)/(6+3v): v=0 → (.500, .167, .333); v=1 → (.444, .222,
  .333); v=3 → (.400, .267, .333); v→∞ → uniform. Every pot size is a
  slightly different metagame.

**Engine deltas**

| Engine | Sustains added | Kills added | Health |
|---|---|---|---|
| Prediction loop | value-skewed frequency bias; a leveling ladder ("she'll chase the 3-pointer → I throw Rock"); pot-modulated moving equilibrium | none (no dominant strategy — script; simultaneity intact) | healthy-but-conditional → **healthy** (one-shot gains a knowledge component) |
| Pattern mastery | learnable non-obvious equilibrium + exploitation ladder; per-pot-size metagames | none | at risk → **healthy** |
| Fellowship | — | minor: scorekeeping (count on fingers) | healthy → healthy− |
| Flow | rising-stakes pot arcs | — | N/A → mild presence |

Cross-engine damage line: the zero-equipment instant-decider niche
(Fellowship) — keep base RPS for coin-flip duty; this variant is the
*game* format.

**Costs**

- Cognitive load: option pool **3 → 3** (Query 1: pass). New state: three
  win values + one pot counter.
- Could damage: Fellowship (above); raw tie frequency rises at fresh pot.
- Implementation scope: **S** — rules text only, prototypable in one recess.

**Identity check**

| Pillar | Verdict | Note |
|---|---|---|
| Simultaneous zero-reactivity | preserved | untouched |
| Balanced intransitive cycle | preserved | script: same cycle, no dominance |
| Small pool / low load | preserved | 3 options |
| Bare-hands ritual | preserved | scores on fingers; no equipment |
| Player symmetry | preserved | identical payoffs both sides |

### P2 — The Well Returns (7-node 2-Paradox: Heptad Solo + Heptad Twin)

**Mechanic spec**

*The chart.* Seven signs on a circle, clockwise:
**Paper → Rock → Poison → Scissors → Water → Fire → Well** (→ Paper).
One rule wires everything: **each sign beats the signs 1, 2, and 4 steps
clockwise from it** (and loses to the other three). This is the
quadratic-residue (Paley) tournament on 7 nodes — the proven-minimal
2-Paradox graph (Query 4). The classic trio sits at positions {0, 1, 3},
so **base RPS is embedded unchanged**: Paper > Rock > Scissors > Paper.

Full edge list (each sign beats 3):

| Sign | Beats | Flavor |
|---|---|---|
| Paper | Rock · Poison · Water | wraps it · blots it dry · the paper boat rides the flood |
| Rock | Poison · Scissors · Fire | seals the vial · blunts them · smothers it |
| Poison | Scissors · Water · Well | corrodes the blades · taints the stream · poisons the well |
| Scissors | Water · Fire · Paper | snips the stream · snuffs the wick · cuts it |
| Water | Fire · Well · Rock | douses it · overflows it · erodes it |
| Fire | Well · Paper · Poison | boils it dry · burns it · burns it clean |
| Well | Paper · Rock · Scissors | swallows it · it sinks · they sink |

The hook: **the Well** — the historically banned fourth throw (French
*puits*) — returns, and it beats *all three* classic signs. The three new
elements (Poison, Water, Fire) are exactly the ones that tame it.

*Gestures* (all one-handed, distinct silhouettes): Rock = fist · Paper =
flat palm down · Scissors = V · Poison = pinky extended · Water = vertical
chop · Fire = fingers splayed upward · Well = thumb-to-fingertips circle
(the classic puits sign).

*Formats.*

- **Heptad Solo** (default): one sign per throw, best of 9. Pool = 7.
- **Heptad Twin** (expert tier): each player throws **two different signs at
  once** (one per hand). All four cross-matchups resolve (+1 win / −1 loss /
  0 same sign); the **sum** is the round margin; positive margin wins, 0 is
  a tie. Pool = C(7,2) = 21 combinations. Twin is the format where the
  2-Paradox does real work: **no pair you field is safe — some single sign
  beats both of your hands, always** (script-verified below).

*Onboarding (act-based escalation, interaction-structure §2.5).*

- **Act 1:** classic trio — everyone already knows it.
- **Act 2 — the reveal:** add the Well. Deliberately broken: the Well
  dominates all three classics (script-verified below). Played as a short
  ceremonial beat — "this is why it was banned" — never competitively.
- **Act 3:** add Poison, Water, Fire — the full heptagon, balance restored.

**Rationale**

- Targets **finding #2** exactly and completely: the audit says the 2-Paradox
  is "the *exact* math fix … but only if you also add multi-node fielding."
  This proposal delivers the wired 7-node chart (verified), the fielding
  mechanic (Twin), and the onboarding — the audit's §6.3 gesture made
  concrete (standing rule 3's own example).
- Targets **finding #3**: tie rate falls from 33.3% to **14.3%** (Solo,
  uniform play) / **23.8%** (Twin, incl. neutral pair-matchups); Pattern
  mastery gains composition depth (design-moves "Amplify: Pattern mastery —
  composition depth: few pieces, many combinations").
- Moves used: **2-Paradox expansion** (Family 1) composed with **Subset
  rotation** (the act structure is its recommended mitigation) and a
  fielding layer.

**Theory-test evidence**

Full heptagon, verbatim (pass bars: dominated none + the exact 2-Paradox
line — both met):

```
Mode: binary | Nodes: 7 (Paper, Rock, Poison, Scissors, Water, Fire, Well)

== STRUCTURE ==
Tournament: yes (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Paper -> Rock -> Poison -> Scissors -> Paper
3-cycles: 14

== DOMINATED NODES ==
Dominated nodes: none

== DOOM-STACKS (unbeatable subsets) ==
size 2: none — the 2-Paradox property holds.

== VIABILITY (eigenvector centrality, steady-state heuristic) ==
  Fire: 0.1429
  Paper: 0.1429
  Poison: 0.1429
  Rock: 0.1429
  Scissors: 0.1429
  Water: 0.1429
  Well: 0.1429
```

| Metric | Base (before) | Heptad (after) | Delta |
|---|---|---|---|
| Dominated nodes | none | none | **pass bar met** |
| Size-2 doom-stacks | 3 (all pairs) | **none — 2-Paradox holds** | finding #2 resolved |
| 3-cycles | 1 | 14 | 14× the counter-play texture |
| Viability | uniform 0.3333 | uniform 0.1429 | symmetry pillar preserved exactly |
| Tie rate (uniform play) | 33.3% | 14.3% Solo / 23.8% Twin | finding #3 improved |

Act-2 teaching subset {Paper, Rock, Scissors, Well}, verbatim — the
brokenness is the *point* of the beat, and it is verified, not asserted:

```
== DOMINATED NODES ==
Paper is DOMINATED by Well (never a better pick).
Rock is DOMINATED by Well (never a better pick).
Scissors is DOMINATED by Well (never a better pick).
```

Twin Throw, pair-vs-pair derived chart (21 pair-nodes; entry = number of
the 4 cross-matchups won). Key lines, verbatim:

```
Mode: weighted | Nodes: 21 (Paper+Rock, Paper+Poison, ... , Fire+Well)
Tournament: no (tournament = every matchup has a winner)
INTRANSITIVE (cycle exists). Example cycle: Paper+Rock -> Paper+Poison -> Paper+Water -> Paper+Rock
3-cycles: 147

== DOMINATED NODES ==
Dominated nodes: none

== DOOM-STACKS (unbeatable subsets) ==
size 2: none — the 2-Paradox property holds.

== VIABILITY ==
  (all 21 pairs): 0.0476
```

So the Twin metagame is itself a balanced intransitive web: **no dominated
pair, no unbeatable pair-of-pairs, perfectly uniform pair viability
(1/21 each)**. Supplementary: margin histogram over ordered pair-matchups
is symmetric ({±3: 21, ±2: 63, ±1: 84, 0: 84}); 84/420 distinct matchups
are neutral, giving the 23.8% tie rate above.

**Engine deltas**

| Engine | Sustains added | Kills added | Health |
|---|---|---|---|
| Pattern mastery | composition depth (21 pairs from 7 signs); layered reveals via acts; 14 3-cycles of matchup texture | option bloat risk (Twin) — mitigated by the 1-2-4 rule + expert gating | at risk → **healthy** (Solo); Twin = deep end |
| Prediction loop | balanced web preserved (script); richer read space ("she leads Well after losing") | load strain in Twin (see costs) | healthy, conditional as before |
| Fellowship | the Act-2 reveal is a designed table moment; still bare hands | 7 gestures to teach | healthy |
| Flow | act escalation = difficulty tracking skill | — | N/A → mild presence |

Cross-engine damage line: Prediction loop is the engine at risk if Twin is
served to novices — the load strain is real; that is what the act gating
and the Solo default are for.

**Costs**

- Cognitive load: Solo pool **3 → 7** — exactly the audit's stated ceiling
  (Query 1: pass at cap). Memorization is compressed by one generative rule
  ("beats 1, 2, 4 clockwise") plus flavor stories — 7-node scale, not
  21-edge rote. Twin decision pool **7 → 21 combinations**; memorization
  unchanged (same 21 edges). Query 1's kill condition is
  interaction-*parsing* overload, which stays at 7-node scale — but the
  choice-space growth is a genuine strain: **flagged, expert-gated,
  playtest question §6.**
- Could damage: Prediction loop (Twin load); onboarding time
  (vs RPSLS as the learnability baseline).
- Implementation scope: **M** — 7 gestures, teaching acts, rules text.

**Identity check**

| Pillar | Verdict | Note |
|---|---|---|
| Simultaneous zero-reactivity | preserved | Solo and Twin both reveal at once |
| Balanced intransitive cycle | preserved | script: 14 cycles, no dominance, uniform 1/7 |
| Small pool / low load | preserved (Solo, at the audit's ≤7 cap) / **strained (Twin)** | rated preserved-with-strain: memorization stays 7-scale; 21-combo choice space is the flagged risk |
| Bare-hands ritual | preserved | 7 one-hand gestures; Twin uses both hands, one countdown |
| Player symmetry | preserved | regular tournament; uniform viability (script) |

### P3 — Throwdown **[Wildcard — identity-stretching]**

**Mechanic spec**

- Components per player: **10 chips**; three throw tokens (Rock / Paper /
  Scissors) — or any commit protocol that locks a throw secretly.
- Each round:
  1. **Ante:** both put 1 chip in the pot.
  2. **Commit:** both secretly and simultaneously lock a throw (token
     facedown under the fist).
  3. **Bet:** the opener (alternates every round) **checks or raises 1
     chip**; the other may **fold, call, or re-raise 1** (maximum 3 raises
     total per round).
  4. **Reveal:** simultaneous. Winner takes the pot.
- **Fold:** concede the pot *without revealing your committed token* — you
  pay chips to deny your opponent behavioral data (mucking).
- **Tie:** pot stays on the table; next round's antes stack onto it.
- **Match:** opponent busted, or biggest stack after 15 rounds.

The twist that makes it RPS and not poker: there is no hand strength —
all throws are symmetric. **A bet can only mean "I have read you."** You
are betting your prediction, and reading their bet for whether the
prediction is real. The throw is locked *before* betting, so betting leaks
nothing you can react to with your hands — only your fold decision and
your future rounds.

**Rationale**

- Targets **finding #1** head-on. The audit's hard ceiling: one-shot vs an
  unreadable opponent is a coin flip. Betting installs skill *inside* a
  single round: fold equity (you can win a round without winning the
  throw), bet-sizing reads, and priced confidence. Query 2 says RPS runs on
  "out-of-band social manipulation (bluffing, rhetoric, tells)" — this
  proposal converts that out-of-band fuel into the actual pipework.
- Targets **finding #3**: a second mastery channel (bet patterns, timing
  tells) on top of throw frequencies; ties snowball the pot instead of
  being dead. Pot growth is throw-agnostic, so it raises stakes *without*
  skewing the throw mix — the base uniform equilibrium of the matrix is
  untouched.
- Moves used: Family 4 wildcards **resolution-timing bend** (reveal delayed
  behind a betting phase) + **information bend** (the new hidden thing is
  *confidence*; the new question is "does that raise mean a real read or a
  bluff?"), composed with systemic-levers **Information structure → Bluff
  bandwidth** ("pull when a prediction engine exists but starves" — the
  audit's exact condition: 'healthy but conditional') and **Economy →
  Sink** (antes/raises as the stake engine).
- Beyond the audit (standing rule 3): no §6 lever touches economy or bluff
  bandwidth.

**Theory-test evidence**

Layer move — the interaction matrix is untouched, so the base-chart run
applies unchanged (see P1's before-column; `Dominated nodes: none`,
1 cycle, uniform 0.3333). Theory anchors, mapped per standing rule 4:

- systemic-levers, *Information structure / Bluff bandwidth*: widening
  bluff bandwidth is the documented lever for a starving prediction
  engine; its documented failure mode ("bluffing dominates system mastery
  entirely") is mitigated by the 3-raise cap and small stacks.
- interaction-structure §1.2: simultaneity of *commitment* is the pillar —
  preserved strictly, since throws lock before any bet.
- interaction-structure §2.1 (iteration): bet history is a second stream of
  behavioral data — "what is this actor's frequency bias" now applies to
  raises and folds too.

**Engine deltas**

| Engine | Sustains added | Kills added | Health |
|---|---|---|---|
| Prediction loop | formalized bluff bandwidth; stakes that make reads pay; two read channels (throw frequency + bet pattern) | risk: bluffing drowns the throw game (capped raises mitigate) | healthy-but-conditional → **healthy+** — the deepest single-round fix for #1 |
| Pattern mastery | bet-sizing tells, timing tells, fold-frequency patterns | — | at risk → **healthy** |
| Fellowship | poker-night spectacle, spectating, table talk is now load-bearing | **decider niche broken**: equipment + ~20-minute sessions | healthy → **bent** — different social occasion |
| Flow | stack-pressure arc, elimination tension | stakes stress kills casual lightness | N/A → present |

Cross-engine damage line: Fellowship's 5-second zero-equipment
fair-decider — fully sacrificed in this variant (that niche stays with base
RPS); casual lightness (Submission) also traded for tension.

**Costs**

- Cognitive load: throw pool **3 → 3**; betting adds decisions with ≤4
  options per phase (Query 1: pass). State: two chip counts + pot.
- Could damage: Fellowship (above); the RPS core risks demotion to a
  randomizer if bet play dominates — the §6 playtest question.
- Implementation scope: **S–M** — chips + tokens + one page of rules.

**Identity check**

| Pillar | Verdict | Note |
|---|---|---|
| Simultaneous zero-reactivity | preserved (strictly) | throw locks before betting; betting cannot react into the throw |
| Balanced intransitive cycle | preserved | matrix untouched |
| Small pool / low load | preserved | 3 throws; small betting tree |
| Bare-hands ritual | **broken** | chips, table, session length — the stretched pillar |
| Player symmetry | preserved | opener alternates; identical stacks |

## 4. Recommendation & sequencing

**Pursue P1 first.** It is the smallest change (scope S, zero components,
option pool unchanged), it attacks the top-severity finding through a
verified mechanism (uniform play becomes exploitable at +2/3 per round), it
repairs the tie problem and the mastery ceiling in the same stroke, and it
preserves every identity pillar. It can be playtested the same afternoon it
is written.

**Compounds:**

- **P1 + P3 → "Throwdown Deluxe."** Weighted wins give bets something to
  price (a committed Scissors is a 3-point threat worth raising on) and the
  two pot mechanics merge cleanly. Natural second step if P1's value layer
  proves out and a table wants the dedicated-game format.
- **P2 is an independent track** (the party/campaign expansion): ship Solo
  as the default, Twin as the tournament tier. It can proceed in parallel —
  it shares no rules text with P1/P3.

**Conflicts:**

- **P1 × P2 — do not stack.** Weighted values on the heptagon would need 21
  per-edge prizes (load explosion) and would de-uniformize the Paley
  balance that the script just certified; both proposals also compete for
  the same Prediction-loop clarity budget.
- **P2-Twin × P3** — load stacking (21-combo choice + betting tree);
  playtest-gated at best, not recommended on paper.

## 5. Re-audit handoff (Path-B spec) — Sharpened Throws

Self-contained rules; auditable cold.

**Players:** 2. **Equipment:** none (scores counted on fingers or aloud).

**Signs:** Rock (fist), Paper (flat hand), Scissors (V).

**Interaction chart** (row vs column; entry = points the row player scores
when that matchup resolves in their favor; all matchups decisive except
mirrors, which tie):

|          | Rock | Paper | Scissors |
|----------|:----:|:-----:|:--------:|
| **Rock**     | tie  |  loses  | **wins, +1** |
| **Paper**    | **wins, +2** | tie | loses |
| **Scissors** | loses | **wins, +3** | tie |

Equivalent zero-sum form: `Rock [0, −2, +1] · Paper [+2, 0, −3] ·
Scissors [−1, +3, 0]`.

**Round:** both players throw one sign simultaneously on a shared countdown
("rock–paper–scissors–shoot"). Zero reactivity; no hidden state other than
intent.

**Scoring:** the round's winner scores their winning throw's value
(Rock 1 / Paper 2 / Scissors 3).

**Tie pot:** every tied round adds 1 point to a shared pot. The next
decisive round's winner scores their throw value plus the entire pot; the
pot then resets to 0. The pot carries no owner and no upkeep.

**Match end:** first player to 7 or more points wins immediately.

**Economy:** the pot is the only stock — sourced 1 per tie, drained fully
on the next decisive round. No other resources, costs, or progression.

**Information structure:** fully open. Simultaneous commitment is the only
information mechanic; scores and pot are public.

> To validate independently, run the game-analysis skill against this
> section in a fresh session, and compare its findings with the audit that
> seeded this redesign.

## 6. Assumptions & open questions

- **Ground truth:** the seed audit (Path A, high confidence) is taken as-is;
  pillars and targets derive from its §2/§4/§5.
- **Directive interpretation:** silence parsed as default boldness and
  default direction (§1). If bolder or differently-aimed proposals are
  wanted ("go bigger", "maximize Fellowship"), say so and the portfolio
  regenerates under that directive.
- **P1 value spread (1/2/3)** is the minimal integer spread; other spreads
  (e.g. 1/2/4) shift the Nash mix and are tunable. Playtest measure: do
  players *feel* the leveling ladder ("they'll chase the 3-pointer") within
  one session?
- **P1 tie rate** rises to ≈38.9% at fresh-pot Nash (from 33.3%). The bet is
  that pot-charged ties read as tension, not dead air. Playtest measure:
  tie-round engagement vs base RPS.
- **P1 pot math** is exact in the chip-scored (zero-sum) model; the
  race-to-7 variant behaves directionally the same but was not solved in
  closed form. Playtest or solve numerically if the distinction starts to
  matter.
- **P1/P2 centrality caveat:** weighted-mode eigenvector centrality reads
  raw scoring power, not play rate (per the script's own docstring); Nash
  mixes quoted above are the strategic reference.
- **P2 learnability:** 7 gestures + 21 edges behind one generative rule.
  Playtest measure: time-to-fluency vs RPSLS (5 nodes) as baseline;
  gesture confusability (Poison-pinky vs Scissors-V) under a fast countdown.
- **P2 Twin load (the flagged strain):** does the 21-combination choice
  space cause analysis paralysis that kills the read? Playtest measure:
  decision time per round and self-reported "I chose by reading them" vs
  "I chose by calculating."
- **P2 size-3 subsets:** unbeatable 3-subsets exist in any 7-node chart
  (3-paradox tournaments require far larger rosters; known constructions
  use 19 nodes). Inert here — no mode fields three signs. Any future squad
  variant must re-run the math, not assume.
- **P3 bluff-drowning risk:** if bet play dominates, the RPS core demotes to
  a randomizer. The 3-raise cap and 10-chip stacks are the paper mitigation.
  Playtest measure: fraction of pots won by folds vs reveals (a healthy
  table should see both in real numbers).
- **P3 protocol integrity:** the commit-before-bet ordering is load-bearing
  (it is what preserves the zero-reactivity pillar). Physical token commit
  is the honest-play mechanism; app implementations get it for free.

---

*Generated from the 2026-07-07 audit; charts and derivations live alongside
this doc's scratch runs. All script output above is quoted verbatim from
`matrix_analysis.py`. This document is theory-consistent, not play-tested.*
