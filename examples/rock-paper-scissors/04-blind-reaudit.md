# Sharpened Throws — Design Audit (fresh session, 2026-07-08)

Produced by the `game-analysis` skill, Path B (read-and-extract), blind to the
seed audit per the spec's validation note. Every quantitative claim below is
**computed, not estimated**: exact rational equilibrium algebra, full
backward-induction DP over match states (score × score × pot, each state's
3×3 zero-sum stage game solved exactly), and a 200k-match seeded simulation.

## 1. Game snapshot

**Sharpened Throws** — 2-player, equipment-free weighted RPS: win values
Rock 1 / Paper 2 / Scissors 3, a shared tie pot (+1 per tie, claimed whole by
the next decisive winner), first to 7 or more points. Material examined:
`sharpened-throws-spec.md` only. Confidence: **high** — the spec is
self-contained and internally consistent; the only analysis approximation is
a DP pot cap of 12, sensitivity-checked at 16 with no change to any reported
figure.

## 2. Typology

| Axis | Verdict | Evidence |
|------|---------|----------|
| Transitive / intransitive | **Intransitive** | `matrix_analysis.py`: "Tournament: yes … INTRANSITIVE (cycle exists). Example cycle: Rock -> Scissors -> Paper -> Rock. 3-cycles: 1" |
| Simultaneous / sequential | **Simultaneous, zero reactivity** | shared countdown (spec); prediction-engine pillar intact (interaction-structure.md §1.2) |
| Symmetric / asymmetric | **Symmetric roles, asymmetric edge weights** | both players have the same 3 options; matrix is antisymmetric (zero-sum), but per-edge values differ (1/2/3) |
| Spatial / abstract | **Abstract** | no board, no positioning |
| Dense / sparse matrix | **Dense** | complete tournament; ties only on mirrors |

**Genre framing:** a two-player zero-sum simultaneous folk duel — the classic
RPS prediction game with a discoverable valuation layer. Per
interaction-structure.md §3.3, dense + mirrored ⇒ competitive prediction
game, not a roster-builder.

## 3. Systems map

**Core loop:** countdown → simultaneous throw → resolve — mirror: pot +1 ·
decisive: winner scores throw value + pot, pot resets → first to ≥7 wins.

**Nodes:** Rock, Paper, Scissors. **Matrix** (zero-sum differential form,
row vs column): Rock `[0, −2, +1]` · Paper `[+2, 0, −3]` · Scissors
`[−1, +3, 0]`.

**Economy:** one stock — the pot. Source: ties (+1 each). Sink: fully drained
by the next decisive winner. Scores are winner-only absorbing counters (no
negative scores). Verified: the pot can never be orphaned — a match can only
end on a decisive round, which drains the pot first.

**Progression gates:** N/A — single self-contained match, no meta.

## 4. Fun engines (ranked)

1. **Prediction loop — curated (interaction-structure.md §1) — healthy,
   strengthened vs classic RPS.** Evidence: simultaneity + script-verified
   balanced 3-cycle + option pool of exactly 3. Sustains: a ~7.5-round match
   gives iteration for behavioral reads (§2.1); open scores/pot make correct
   play *state-dependent*, adding "does my opponent know this state?" as a
   read dimension; full out-of-band bluff bandwidth (Query 2). Kills: an
   opponent executing the true mixed equilibrium reduces it to a fair coin —
   inherent to the genre, and harder to do here because the correct mixes are
   skewed and keep shifting with pot and score.
2. **Pattern mastery — Koster, *A Theory of Fun* — healthy; the biggest
   upgrade over classic RPS.** Evidence: a quantified mastery ladder with
   measured floors (guaranteed match-win probability vs a perfect exploiter):
   uniform habit **0.183** → static base mix **0.325** → pot-adjusted mix
   **0.378** → match-optimal **0.500**. The strata are learnable in order:
   weights → base mix (½, ⅙, ⅓) → pot adjustment (flatten toward uniform as
   the pot grows) → endgame tables. Kills: the endgame tables are finitely
   memorizable (chess-endgame-like); the exploitation layer above them never
   closes.
3. **Flow — Csikszentmihalyi — healthy for matched players; at risk on first
   contact (see I-1).** Evidence: instant resolution, one clear goal; match
   length P10 5 / P50 7 / P90 10 rounds (mean 7.49); built-in tension spikes —
   the 4–4 standoff ties with probability >50%, feeding the pot and
   escalating stakes.
4. **Fellowship — MDA — ambient.** Table talk and shared pot drama support
   party play; present, not dominant.

## 5. Diagnosis

### [Matrix]

Clean bill, script verbatim: **"Dominated nodes: none"**; single 3-cycle;
tournament complete. All three nodes sit in the exact equilibrium support —
mix **Rock ½, Paper ⅙, Scissors ⅓**, every pure throw EV 0 (Nash, game
value 0). No live matrix-layer issues.

### [Spatial]

N/A — abstract game, no spatial layer.

### [Information]

- **I-1 · High · live — the knowledge cliff.** A classic-RPS-habituated
  (uniform) player loses **0.817 : 0.183** to an opponent who merely knows
  the weighted math and best-responds — zero psychological reads required.
  In classic RPS uniform is unexploitable; here nothing in the rules signals
  that it has become wrong. First contact between unequal-knowledge players
  is a stomp the loser cannot diagnose. Dual nature: discovering the mix *is*
  the game's content — the lever must diffuse knowledge without deleting
  discovery (L-1).

### [Tempo]

- **T-1 · Low · live — nothing rises above Low.** Pacing verified healthy:
  mean 7.49 rounds, P90 10, max 20 across 200k matches; ~2.8 ties/match. Tie
  chains are self-damping — as the pot grows, correct mixes flatten toward
  uniform, so the equilibrium tie probability *falls* (0.389 at pot 0 → 0.335
  at pot 10). Endgames accelerate because more throws become lethal.

### [Systemic]

- **S-1 · Medium · live — Paper reads as a dead button.** Correct Paper
  frequency is ⅙ (Paper mirrors are 1/14 of ties); players will feel "Paper
  is bad" and drift into Rock-heavy metas. The system already self-corrects:
  Rock mirrors are 9/14 of ties, Rock standoffs pump the pot, and the pot is
  Paper weather — the correct Paper share rises with the pot (0.167 → 0.306
  at pot 10), and a Paper snipe collects 2 + pot. Residual risk is
  presentation, not mechanics (L-2).
- **S-2 · Low · live — shield and sword are separate, and there is a hidden
  shark ceiling.** Equilibrium play does not passively punish bad play in
  match terms: static-eq vs uniform = **0.498**, pot-adjusted vs uniform =
  **0.499** (slightly *below* 0.5 — race granularity). Punishment requires
  deliberate deviation (best response vs uniform = 0.817). The per-round
  theory is also not match-safe: at pot k the static base mix leaks k/6 per
  round to both Rock and Paper (EV(R) = EV(P) = +k/6, EV(S) = −k/3 against
  it), floor 0.325; even the fully pot-adjusted player's floor is only
  **0.378** against a full match-DP opponent, the gap living entirely in
  score-state play. For a folk game this is invisible depth — flagged so it
  is a known property, not a surprise.
- **Economy & feedback — clean.** Single self-draining stock, inflation
  impossible; E[pot claimed per decisive round] ≈ 0.60, P(match sees pot ≥ 3)
  ≈ 0.22. No snowball — winning grants nothing forward; the pot is
  ex-ante-neutral variance that relatively favors the trailer: honest
  comeback pressure without handouts. No sandbagging incentive. A 6–0 lead
  wins 0.890 — commanding, not a lock.

### Structural notes (true but inert — do not outrank live issues)

- **N-1 [Matrix]** — script verbatim: all three 2-subsets are unbeatable
  ("2-Paradox property does NOT hold"). True of every 3-cycle; inert because
  the game fields one throw per round — there is no stacking layer for a
  doom-stack to live in.
- **N-2 [Matrix]** — the script's eigenvector viability (Scissors 2.54 >
  Paper 0.22 > Rock −1.76) *inverts* actual equilibrium usage (Rock ½ >
  Scissors ⅓ > Paper ⅙). The raw-payoff heuristic misreads weighted RPS:
  sharpening an edge suppresses the *victim's* frequency, so the +3 prize is
  claimed at the lowest rate (1/18 per round vs 1/6 for Rock's +1). Use
  equilibrium usage, not centrality, for balance claims here. Hidden
  elegance: at equilibrium every edge carries identical expected points (1/6
  per ordered edge) — and this equalization holds for *any* weight triple,
  so tuning the weights can never make aggregate scoring lopsided.
- **N-3 [Tempo]** — tie streaks are unbounded in principle (no terminating
  rule); with P(pot ≥ 3) ≈ 0.22 per match and a 200k-match maximum of 20
  rounds, no rule is needed.
- **N-4** — the endgame is exactly solvable and partially memorizable:
  (6,6,·) is uniform classic RPS — the design converges to its ancestor at
  double match point; (6,5,0) leader plays (⅓, ⅙, ½) for V = 7/12; one tie
  later, (6,5,1) snaps to uniform because the trailer's Rock becomes lethal;
  (4,4,0) is a Rock standoff (0.664/0.112/0.224, >50% tie) cascading through
  (4,4,1) = (0.428/0.144/0.428) to uniform at (4,4,2). Mastery content, not
  a defect. Note also: the match-optimal opening (0.508/0.161/0.331) is
  nearly the intuitive base mix — the theory answer is honest at 0–0.

## 6. Improvement levers

- **L-1 → I-1 (information lever — smallest sufficient).** Print the street
  odds on the rules card: *"Streetwise: about half Rock, a third Scissors,
  the rest Paper — then read your opponent."* Predicted effect: collapses the
  0.817 arithmetic stomp toward reads-based play; level-1 knowledge becomes
  common and the contest moves to levels 2+ (pot and state adjustments stay
  discoverable). Cost: zero mechanics, zero option-pool delta; spends some
  discovery joy — print as a skippable "coach's note" for purists. Heavier
  alternatives (handicaps, mandated tutorial matches) rejected.
- **L-2 → S-1 (framing lever, zero-mechanical).** Name Paper's role: *"the
  ambush — rare by design; a fat pot is Paper weather."* Aligns felt identity
  with the true dynamics. No mechanical buff: the pot already self-corrects
  Rock stalemates, and buffing Paper's value would only re-shuffle the same
  frequency inversion (N-2).
- **L-3 → S-2/N-4 (optional content, not rules).** An enthusiast appendix of
  3–4 exact endgame states, chess-endgame style — converts hidden shark edge
  into published mastery content. Cost: zero mechanics; slight "solved" aura,
  so keep it out of the base rules.
- **L-4 → onboarding hygiene.** Add one worked example to the pot rule
  ("two ties, then Paper wins: score 2 + 2 = 4"). Cost: zero.
- **L-5 → anti-lever (explicit).** Do **not** add a 4th sign, throw costs, or
  a pot cap. The option pool is the scarcest budget (interaction-structure.md
  Query 1); the design's core achievement is real depth at exactly 3 options,
  and 4-node graphs reopen neutrality/even-cycle problems
  (analysis-workflow.md §2–3).

## 7. Assumptions & open questions

- DP pot cap 12 (identical results at cap 16); the real pot is unbounded —
  negligible tail.
- Two equilibrium senses are used and labeled: per-round differential
  (exact rationals) vs match-win-optimal (DP). The per-round game treats a
  round as zero-sum in score swing; the real object is match-win probability.
- Human-behavior claims (skewed mixes are hard to execute unaided; Paper
  perception drift) are design-psychology reasoning in the Query-2 tradition,
  not measurements — confirm in playtests.
- This audit is blind to the seed audit; the comparison is the designer's
  step.
- Rules ambiguity scan: none found needing a ruling — winner-only scoring,
  "7 or more" handles overshoot, only one player can score per round (no
  simultaneous crossing), the pot is always claimed by match end.
- Reproducibility: simulation seed 42, 200k matches; verification scripts in
  the session scratchpad.

---

**Verdict:** structurally sound and verified — intransitive core intact, no
dominated nodes, self-draining economy, honest comeback texture, ~7.5-round
matches, and a measured four-rung mastery ladder (0.183 → 0.325 → 0.378 →
0.500) that classic RPS entirely lacks. One High finding (first-contact
knowledge cliff) and one Medium (Paper perception), both fixable with printed
words rather than rules. The strongest recommendation is the anti-lever:
change nothing mechanical.
