# Tetris — Deep Design Audit

*Method: `game-analysis` skill, full 8-step procedure. Framework claims are attributed to the skill's reference files (`interaction-structure.md`, `fun-engines.md`, `systemic-levers.md`, `analysis-workflow.md`) or to named canonical sources. Standing rule 1 observed: the interaction matrix is diagnosed first, and every claim that leans on space, tempo, or information declares that layer explicitly.*

---

## 1. Game snapshot

- **Title:** Tetris (Alexey Pajitnov, 1984→). Analyzed as a family, with two reference points:
  - **Classic** — NES / Game Boy era (1989), original rotation, no hold, unbounded-ish randomizer.
  - **Guideline** — The Tetris Company's standardized ruleset (~2001–2006→): Super Rotation System (SRS), 7-bag randomizer, hold, ghost piece, 6-piece next queue, T-spins, back-to-back, combos, perfect-clear bonuses (Tetris Worlds, Tetris DS, Tetris Effect, Tetris 99, Jstris, modern Tetris.com).
- **Intake path:** A (recall-and-verify). Rules are fully public and structurally stable across versions.
- **Confidence:** High on structure (piece set, 10-wide board, line-clear rule, level→gravity ramp, randomizer designs, SRS/hold/T-spin as guideline additions). Version-specific *numbers* (scoring constants, lock-delay ms, DAS/ARR frames, buffer-row count) are parked in §7 — the design conclusions do not depend on their exact values.

---

## 2. Typology *(interaction-structure.md §3)*

| Axis | Verdict | Evidence |
|------|---------|----------|
| **Transitive / intransitive** | **N/A (degenerate)** | The 7 tetrominoes have **no edges to each other** — no piece "beats" another. There is no tournament graph to be transitive *or* intransitive. Pieces are non-competing tools applied to terrain. This is the single most important classification fact: Tetris sits *off* the framework's primary axis (interaction-structure.md §1 assumes opponent-vs-opponent counterplay). |
| **Simultaneous / sequential** | **Real-time sequential** | Pieces arrive one at a time, but under a *continuous falling clock* — not turn-based. Gravity is a real-time pressure, not a turn. Versus modes (Tetris 99, PPT) are **real-time concurrent**: players build in parallel, coupled only indirectly through garbage. |
| **Symmetric / asymmetric** | **N/A (no matrix); if forced, asymmetric** | No interaction matrix to mirror (interaction-structure.md §3.3). Roles are non-interchangeable: the player *arranges*, the generator *supplies*. The generator is a neutral, non-strategic dealer — under 7-bag it is provably fair (equal distribution), so the *fairness* reading is "symmetric-vs-neutral-environment." Versus modes are symmetric (mirror rules, shared piece distribution). |
| **Spatial / abstract** | **Overwhelmingly spatial** | This is the **dominant layer**. Tetris is close to pure spatial reasoning (2D packing on a 10-wide grid) plus a real-time execution layer. Almost the entire game lives here. |
| **Dense / sparse matrix** | **N/A** | No node-vs-node matrix exists. |

**Genre framing implied:** Tetris is a **real-time spatial-packing optimization game** (falling-block puzzle-action), *not* an intransitive prediction game. Its challenge is spatial combinatorics under (a) an accelerating clock, (b) bounded stochastic supply, and (c) a dexterity/finesse execution ceiling. Any "prediction" is **self-directed** — anticipating *your own* future supply and planning multi-piece placements — never opponent-directed. The RPS-style "prediction engine" (interaction-structure.md §1) is essentially absent; see §4.

---

## 3. Systems map

### Core loop
`randomizer emits tetromino → player perceives board + next-queue + hold → plans target column/orientation → executes (translate · rotate · wall-kick · soft/hard-drop · hold) → piece locks (becomes terrain) → resolve (full rows clear; scoring; back-to-back/combo update; in versus, garbage sent/received) → stack shrinks on clear, gravity may increase on level-up → repeat until spawn is blocked (top-out)`

### Node set
The **7 one-sided tetrominoes**: I, O, T, S, Z, J, L. (Tetris uses 7 rather than the 5 *free* tetrominoes because it treats chiral mirror pairs S≠Z and J≠L as distinct.) They carry **no stats** — only shape. Secondary "nodes" that matter are emergent terrain: the **stack**, individual **rows** (the resource being completed), **holes** (covered empty cells = debt), and, in versus, injected **garbage rows**.

### Interaction matrix
**No matrix — pieces do not interact with pieces.** Building a win/loss matrix here would be garbage-in: the dominance / doom-stack / transitivity analysis in `scripts/matrix_analysis.py` is defined on a versus tournament graph that Tetris does not possess (Step 3 & 6a escape-hatch: "if no interaction matrix exists, say so and continue"). Step 6a is therefore **N/A** and the script is not run.

The closest honest analog is a **piece × terrain-affordance** relationship — how forgiving each piece is on a general surface, and what unique terrain each resolves. This is *not* a symmetric versus matrix (no reciprocity, no "beats"), so it feeds diagnosis qualitatively rather than through the matrix tool:

| Piece | Flexibility | Unique role / cost |
|-------|-------------|--------------------|
| **I** | High + unique power | Only piece that clears **4 rows at once** (a "Tetris") and the only one that fills a **1-wide × 4-deep well**. The strategic *release valve*. Its scarcity is the game's central gamble. |
| **T** | High (esp. Guideline) | Fits many notches; **uniquely enables T-spins** under SRS wall-kicks — the hero piece of modern scoring. |
| **J / L** | High | Chiral pair; fill corners and depth-2/3 notches; comfortable on both flat and stepped surfaces. |
| **O** | **Low** | Rigid 2×2, one orientation; needs a 2-wide flat area; contributes nothing to odd/stepped terrain. The awkward filler. |
| **S / Z** | **Lowest — the "problem pieces"** | Zig-zag shape resists flat placement; laid flat they create an overhang/hole. They require pre-existing *stepped* terrain or vertical placement. Chief source of holes and top-outs (the game's core "grit"). |

### Economy flows *(Machinations vocabulary — Adams & Dormans, `systemic-levers.md`)*
Tetris runs an **inverted economy**, which is its defining and unusual feature:

- **The scarce resource is empty board space** (≈10×20 = 200 cells of buffer).
- **Faucet (source of pressure):** every piece *injects 4 cells of terrain* into that space, at a rate the clock forces ever faster. This is a faucet pointed *at the player*, not a reward.
- **Sink (the only drain):** **line clears.** Completing a row reclaims 10 cells. Clearing is skill- and supply-capped (you must first fill 10 columns to clear 1 row, and you need the right pieces).
- **Multiplier/secondary currencies (Guideline):** score, and the *back-to-back* and *combo* states — a multiplier resource you build up and spend by stringing Tetrises/T-spins/consecutive clears. Perfect-clear (all-clear) is a rare jackpot sink.
- **Net balance:** the pressure-faucet accelerates without bound (gravity → ∞); the drain is capped by human dexterity. **For any human, faucet-pressure eventually exceeds max drain → every endless game ends in a loss.** Tetris is *designed to be lost*; the only question is score/duration. (Rigorous basis: Brzustowski 1992 and **Burgiel 1997, "How to Lose at Tetris"** — a sufficiently long alternating S/Z sequence forces a top-out regardless of play, and a random sequence produces one with probability 1. See §5 for the 7-bag consequence.)

### Progression gates
A **pure speed treadmill**: `level = f(lines cleared)` (classically +1 every 10 lines), and `level → gravity speed`. No unlocks, no content gates, no stat growth — the *only* thing that escalates is the clock. This makes the difficulty ramp and the flow engine the same dial (§4).

---

## 4. Fun engines *(fun-engines.md; ranked by share of play time)*

**1. Flow — Csikszentmihalyi 1990 — evidence: level→gravity ramp.**
The master engine. Clearing lines raises the level, which raises speed, which raises challenge to match rising skill — challenge ≈ skill is *engineered directly* by the progression gate. Clear goals (complete rows), immediate feedback (instant clears, sound, the stack visibly dropping), perfectly readable state (the whole grid is always legible). The "Tetris effect" (players hallucinating falling blocks afterward) is flow bleeding into perception.
- **Sustains:** readable state; sub-second feedback loop; difficulty auto-tracks skill via the level system.
- **Kills:** difficulty *spikes* (see §5 kill-screen) or *plateaus* (speed caps too low for an expert).
- **Health: healthy (Guideline) / at risk (Classic)** — the NES level-29 wall is a discontinuous spike that breaks the channel.

**2. Pattern mastery — Koster, *A Theory of Fun* 2004 — evidence: surface-reading + placement planning.**
The brain consuming learnable spatial patterns: reading surface roughness, matching piece to gap, planning multi-piece sequences, then (Guideline) memorizing openers, T-spin setups, and perfect-clear loops. Depth reveals layers over years (basic stacking → clean/flat stacking → 9-0 well + Tetris → T-spins → PC loops).
- **Sustains:** fresh surfaces at the edge of competence, generated continuously by bounded randomness; **very low output-randomness** (piece *order* is the only randomness; placement is deterministic) → clean skill signal.
- **Kills:** *solved* patterns. Because output noise is so low, the risk is the opposite of most games — at the ceiling the game becomes *too* solvable (see §5).
- **Health: healthy for ~99% of players / at risk at the elite ceiling.**

**3. Tension-and-release (Sensation + Challenge) — MDA (Hunicke, LeBlanc & Zubek 2004) — evidence: the well-and-Tetris risk/reward + audiovisual juice.**
The stack rising is mounting tension; the 4-line Tetris (or a big T-spin) is explosive release. The player *self-regulates* their tension by choosing how greedily to build (safe singles = low tension/low reward; a 9-columns-deep well waiting on the I = high tension/high reward). Juice amplifies the release: Korobeiniki accelerating with speed, the line-clear flash, Tetris Effect's synesthetic feedback.
- **Sustains:** the reward gap between safe and greedy play; satisfying release feedback.
- **Kills:** release *denied by luck* (a drought that kills your well) reads as betrayal, not challenge; or tension so constant it becomes undifferentiated stress.
- **Health: healthy (Guideline; 7-bag protects the payoff) / at risk (Classic; droughts deny release).**

**4. Competence / skill expression — Ryan & Deci (Self-Determination) — evidence: score, level, rank, optional techniques.**
Visible growth: score, level reached, lines, Tetris 99 rank; and *expressive* optional techniques (T-spins, B2B, combos, PCs) let players choose a style — survival vs. max-score vs. speed (autonomy).
- **Sustains:** high ceiling; legible growth; genuinely viable alternative playstyles.
- **Kills:** *illusory* choice (a scoring system where "only Tetrises matter" flattens expression); *hidden* ceilings — the finesse/DAS execution layer is a large, unsurfaced competence wall (§5).
- **Health: healthy, with one opaque wall (finesse legibility).**

**5. Submission (pastime) — MDA — evidence: instant-restart endless loop.**
For casual players, the archetypal low-stakes, infinitely replayable "just one more game." Bite-sized, no narrative commitment, soothing.
- **Sustains:** instant restart; short sessions; a comfortable rhythm.
- **Kills:** a speed ramp that forces stress too early with no relaxed option.
- **Health: healthy** (most versions offer level select / relaxed modes).

**Peripheral / absent (worth naming):**
- **Prediction loop (opponent anticipation) — interaction-structure.md §1 — largely ABSENT.** No opponent in solo. Versus adds only a *light* form (read opponents' boards, time/target attacks) — a resource-race with target selection, **not** the simultaneous RPS bluff. The framework's flagship engine is a minor guest here.
- **Fantasy / Narrative — N/A.** Tetris is famously abstract with no fiction. This is a *strength* (universality, instant legibility), not a gap.
- **Discovery** minimal (historically, techniques like T-spins were *discovered* then codified; Tetris Effect adds cosmetic stage discovery). **Fellowship** only in modern versus. **Expression** moderate in Guideline, low in Classic.

---

## 5. Diagnosis *(severity-ordered; matrix layer first per standing rule 1)*

**[Matrix] — N/A.** No node-vs-node interaction matrix exists (§3). No dominated-node, doom-stack, or transitivity findings are possible or meaningful. The piece-flexibility asymmetry (S/Z and O are "costly," I and T are "powerful") is an *affordance* asymmetry against terrain, not a versus-dominance one; it is diagnosed at the spatial layer below.

**Finding 1 — [Tempo] The kill-screen difficulty spike (Classic).** *Severity: High for Classic; resolved in Guideline.*
NES gravity reaches ~1 row per frame at **level 29**, which outpaces the Delayed-Auto-Shift (DAS) input system — a piece falls faster than you can slide it across the board. This is a *discontinuous* wall, not a smooth ramp: challenge jumps far above skill overnight (fun-engines.md: Flow's kill condition = difficulty spike). Notably, the community later *defeated* the design's assumption by inventing new inputs — **hypertapping**, then **rolling** (drumming the controller back, ~20+ Hz) — pushing past 29 to the true integer-overflow crash (~L155). That players had to invent techniques the designers never anticipated is itself evidence of an execution wall baked into the ramp.

**Finding 2 — [Tempo] The lock-delay "infinity" exploit.** *Severity: High if unpatched; resolved in Guideline.*
Lock delay (a grace period after a piece lands, so you can still slide/rotate it) is a great *feel* lever — but naive implementations let a player reset the timer indefinitely by repeatedly moving/rotating, **stalling the clock forever**. Since the accelerating clock *is* the core engine (§3, §4), infinity defeats the entire game. A feel lever undermining the pressure economy.

**Finding 3 — [Information / Systemic] The randomizer trade-off (two-sided).** *Severity: Medium.*
- *Classic randomizer* (roll, reroll once on immediate repeat) has **no drought protection** — long I-piece droughts are possible. For well-strategy (committing to a deep well, then waiting on the I) this is an *output-randomness-on-an-irreversible-decision* feel-bad (`systemic-levers.md`, Randomness placement): you commit, then the game withholds the payoff. Rigorously, unbounded random input makes loss *inevitable* (Burgiel 1997) because it can flood you with alternating S/Z.
- *7-bag* (each bag = a permutation of all 7) bounds drought to ≤~12 placements between copies of a piece and lets you *count* the near future. It nearly eliminates unfair deaths — **and, subtly, it removes Burgiel's adversarial S/Z flood, so 7-bag Tetris is not provably unwinnable; indefinite survival is theoretically possible for perfect play.** But the same predictability enables *solved* openers (feeds Finding 4). You cannot have both fairness and freshness from one randomizer.

**Finding 4 — [Systemic / Pattern-mastery] Solved patterns at the ceiling.** *Severity: Medium (elite only).*
With 7-bag + hold + near-perfect information + near-zero output randomness, opening theory and perfect-clear loops become *memorizable* and downstacking heuristics converge (fun-engines.md: Pattern-mastery kill = solved patterns). At the very top, decision content thins and solo Tetris becomes a near-pure **execution race** — which is precisely why the competitive center of gravity migrated to *versus* (Tetris 99), where an opponent's garbage keeps reshaping the board. Irrelevant for ~99% of players; it is the *shape of the ceiling*, not a floor problem.

**Finding 5 — [Spatial] The S/Z parity tax.** *Severity: Medium (persistent, arguably a feature).*
On a 10-wide board, S and Z pieces have a parity mismatch with flat ground: laid flat they always leave an overhang, forcing either a hole or a bump. Clean use requires pre-built stepped terrain or vertical placement. Consequence: novices bleed holes from S/Z (holes are near-permanent debt — uncoverable until everything above clears), while experts turn S/Z handling into a mastery layer. This is simultaneously the top source of feel-bad *and* a genuine depth generator — the "grit" of the game. Design tension, not a clean bug.

**Finding 6 — [Tempo / Systemic] The hidden execution ceiling (finesse/DAS opacity).** *Severity: Medium-High, persistent across all versions.*
Horizontal movement is governed by DAS (delay before auto-repeat) and ARR (auto-repeat rate), and "finesse" is placing each piece in the minimum number of inputs. This is a large skill layer that the game **never surfaces**: it teaches *placement* (via the ghost piece) but not *input economy*. Players plateau as gravity climbs — knowing the right placement but unable to execute it fast enough — with no feedback explaining why. A competence-killer (fun-engines.md: Self-Determination) hidden behind an opaque wall.

**Finding 7 — [Systemic] Versus garbage snowball.** *Severity: Medium (versus modes only).*
Receiving garbage raises your stack → less room to maneuver → you clear less and send less → you receive relatively more → snowball to KO. A positive feedback loop (`systemic-levers.md`, Feedback loops) that can make comebacks feel fake and losers feel like spectators. Modern versus already carries mitigations (garbage offsetting/canceling, incoming-garbage delay + telegraph, target-spreading in battle royale) — the diagnosis is that these must be *tuned*, since the raw loop is runaway.

**Not a bug — worth naming: the unwinnable inverted economy (§3).** Unlike almost every other game, Tetris faucets a resource *at* the player into a space they must keep draining, and the faucet always wins in the end. The "you will lose; play well anyway" existential loop is a deliberate and defining choice, not a defect.

---

## 6. Improvement levers *(smallest sufficient lever → predicted effect → risk/cost incl. cognitive-load delta; `systemic-levers.md` + interaction-structure.md §2)*

**F1 — kill-screen spike** → **smooth the gravity curve + add lock delay + cap effective speed at "survivable-with-finesse" (20G).** *Effect:* challenge asymptotes instead of spiking; the flow channel extends indefinitely, so games end from *board-management* failure rather than input-impossibility. *Cost:* removes the "legendary wall" prestige (NES purists preserve the spike as a badge of honor); **zero cognitive-load / option-pool change.** — This is the lever the Guideline already pulled; the trade is accessibility vs. iconic hardship.

**F2 — infinity exploit** → **cap lock-delay resets (move/rotate reset limit, ~15, or hard-lock after cumulative time).** *Effect:* restores the clock's authority (tempo engine intact) while keeping enough grace for finesse and spins. *Cost:* essentially none; a purely corrective lever — the textbook "smallest lever that fixes the diagnosis." Already standard in Guideline.

**F3 — randomizer trade-off** → keep **7-bag as default** (broad audience: fairness, bounded drought) and **offer a TGM-style history randomizer as a ranked/variant mode** (reroll if the piece is among the last *n* drawn, bounded tries). *Effect:* default preserves fair payoffs (protects the Tension-Release engine); the variant blunts deterministic openers, restoring freshness for players who want less solvability (addresses F4 without touching the default). *Cost:* slightly higher variance in the variant; **no change to the option pool** (same 7 pieces); competitive purists may resist a non-symmetric variant — hence *mode*, not default.

**F4 — solved ceiling** → **periodic re-planning pressure**: for solo, a "garbage rain"/cheese or randomized-starting-terrain mode; for competitive, keep the *versus* mode as the flagship (an opponent's garbage is the natural, continuous re-planning generator). *Effect:* feeds the Pattern-mastery engine novel surfaces at the top, keeping *decision* content alive alongside execution. *Cost:* changes the mode's character (less "pure marathon") → ship as a distinct mode; **no cognitive-load increase to the core.** *Note:* the ecosystem already self-corrected by making Tetris 99 the competitive center.

**F5 — S/Z parity tax** → **do not "fix" it; surface it.** Add an opt-in *stacking trainer* that highlights S/Z-friendly step placements and flags hole-creating drops. *Effect:* converts an invisible skill cliff into a teachable gradient while preserving the depth the parity friction generates. *Cost:* trivial UI; **opt-in, so zero load on default play.** (Removing the parity friction outright — e.g., banning S/Z or adding a "flat" piece — would gut a core depth generator; rejected as too large a lever.)

**F6 — hidden execution ceiling** → **make the input layer legible**: in-client finesse feedback (flash when a placement used more inputs than optimal), a DAS/ARR tuning screen with presets, and a short finesse tutorial. *Effect:* turns the opaque wall into a visible, trainable gradient → smooths the mastery curve (Flow) and repairs Competence (Self-Determination). *Cost:* minor UI; gate behind a practice mode so the surfaced complexity does not intimidate casual players; **near-zero core cognitive-load** (opt-in feedback, not new rules).

**F7 — versus snowball** → **tune the existing dampeners**: garbage *offsetting* (outgoing clears cancel incoming before it solidifies) + a short *delay + telegraph* on incoming garbage (a reaction window) + *target-spreading* so no single player is deterministically dogpiled. *Effect:* a controlled negative-feedback / rubber-band lever that dampens runaway and preserves comeback tension. *Cost:* raises versus **option-pool and cognitive-load** (players must learn offsetting and targeting) and, if over-tuned, makes leads feel fake (the opposite failure) — so tune the delay window rather than adding mechanics.

---

## 7. Assumptions & open questions

- **Scope.** Primary lens = modern **Guideline**; **Classic** (NES/GB) is contrasted where the design diverges. Where a claim is version-specific it is tagged (Classic) / (Guideline).
- **Version-specific numbers, parked (not load-bearing to the conclusions):**
  - *Scoring constants.* Classic NES ≈ 40 / 100 / 300 / 1200 × (level+1) for single/double/triple/Tetris. Guideline ≈ 100 / 300 / 500 / 800 × level, with T-spins ~400–1600, back-to-back ≈ ×1.5, combos ≈ 50 × combo × level, perfect-clear bonuses ~800–3500. Exact values differ per title.
  - *Lock-delay reset cap* (~15 moves), *DAS/ARR* frame values, and *next-queue length* (1 in early Classic; 6 in Guideline) vary by client.
  - *Board height.* 10-wide is invariant and load-bearing (10 columns + a 4-long I-piece is *why* the max clear is 4 and why a 1-wide well needs the I). Visible height ≈ 20 (NES); some Classic variants differ (e.g., Game Boy visible height); Guideline adds ~20 buffer rows above (≈40-row matrix). Only the 10-wide fact is relied on.
  - *7-bag max drought* stated as ≤~12 placements between two copies of a piece (illustrative).
- **Unverified attributions (soft confidence):** the "rolling" technique era and the exact level of the NES integer-overflow crash (~L155) are cited from community history, not primary sources. Brzustowski (1992) and Burgiel (1997) are cited from mathematical literature; the *inference* that 7-bag structurally escapes Burgiel's adversarial S/Z flood (→ 7-bag not provably unwinnable) is my reasoning from the bag constraint, not a cited theorem.
- **Out of scope:** economy/scoring of specific spin-offs (Tetris Effect's Zone mechanic, Puyo Puyo Tetris cross-play balance, Tetris 99's badge/targeting meta) — each would merit its own pass; only the shared core is audited here.
- **Fact to verify if this goes further:** whether any shipped Guideline scoring system makes non-Tetris/non-T-spin clears strictly dominated (which would confirm Finding-4-adjacent "illusory choice" in the Competence engine).

---

## Methodological coda — framework fit *(for the skill, not the game)*

Tetris is a clean stress-test of the `game-analysis` skill because its interaction core is **empty**: no node-vs-node matrix, so the transitive/intransitive, symmetry, matrix-density axes and `matrix_analysis.py` all return N/A, and the RPS-derived *prediction engine* (interaction-structure.md §1) is peripheral. The skill handled this correctly — Step 3's "no matrix, say so and continue" escape-hatch and Step 6a's conditional invocation kept the analysis honest, and the entire diagnostic load shifted to `fun-engines.md` (Flow, Pattern-mastery, Tension-Release) and `systemic-levers.md` (inverted economy, difficulty curve, randomness placement, feedback loops). Takeaway for the skill: the interaction-core modules are the *specialized* half; for spatial/solo/economy-driven games the fun-engine and systemic-lever modules are load-bearing, and the typology table earns its keep precisely by *ruling the matrix out* fast.
