# Rock Paper Scissors — Systems Breakdown

## 1. Snapshot

Base RPS (Path A, high confidence — rules fully public and verified against the
game-analysis skill's reference set). It is the *atomic* prediction game: the
smallest possible balanced intransitive contest, and the unit that every
counter-triangle in fighting games, RTS, and TCGs is built from.

## 2. Typology

| Axis | Verdict | Evidence |
|------|---------|----------|
| Transitive / intransitive | **Intransitive** | Beats-graph cycles: Rock→Scissors→Paper→Rock (1 three-cycle) |
| Simultaneous / sequential | **Simultaneous** | Both throw at once; zero-reactivity (interaction-structure §1.2) |
| Symmetric / asymmetric | **Perfectly symmetric** | Uniform viability 0.333 each; every node structurally identical |
| Spatial / abstract | **Abstract** | No board, no positioning |
| Dense / sparse matrix | **Maximally dense** | Complete tournament — every matchup has a winner, zero neutrals |

**Genre framing:** the irreducible **psychological prediction game** — a
1-Paradox (every node beaten by exactly one other), and 3 nodes is the smallest
graph that achieves it.

## 3. Systems map

- **Core loop:** both players simultaneously choose one node → reveal at once →
  resolve by fixed rule → (optionally) repeat for best-of-N.
- **Node set:** {Rock, Paper, Scissors}.
- **Interaction matrix** (row result vs. column opponent; +1 win, −1 loss, 0 tie):

|          | Rock | Paper | Scissors |
|----------|:----:|:-----:|:--------:|
| **Rock**     |  0   |  −1   |   +1     |
| **Paper**    | +1   |   0   |   −1     |
| **Scissors** | −1   |  +1   |    0     |

- **Economy flows:** N/A — base RPS has no resources.
- **Progression gates:** N/A — no progression.

## 4. Fun engines (ranked)

- **Prediction loop** (curated, interaction-structure §1) — *the* engine.
  Sustained by out-of-band reads (bluffing, tells, frequency bias); killed by a
  dominant strategy (impossible here) or broken simultaneity.
  **Health: healthy but conditional** — it only fires with a readable/repeated
  opponent.
- **Fellowship** (MDA) — the countdown ritual and face-to-face stakes are why
  RPS survives as a real-world fair-decision tool. **Health: healthy** in its
  social niche.
- **Pattern mastery** (Koster) — thin third; real only in iterated/competitive
  play (frequency reads, gambits like the "Avalanche" = three rocks).
  **Health: at risk** — shallow ceiling.
- **Flow / Self-determination** — largely N/A (no difficulty curve, no builds).

## 5. Diagnosis (severity-ordered)

1. **[Information] Single-shot collapse to pure chance.** Against an unreadable
   opponent in one round, the game is a coin-flip — Nash-optimal play is uniform
   1/3, and eigenvector viability is exactly equal (0.3333 each). Skill exists
   *only* across iterations, where humans leak exploitable frequency bias. This
   is the hard ceiling on RPS's depth.
2. **[Matrix] All three 2-node subsets are "unbeatable" — the 2-Paradox property
   fails.** **But this is mechanically inert in base RPS:** you throw one node
   per round, never field a pair, so no opponent is ever asked to beat two of
   your throws at once. It is a structural inevitability of a 3-node graph, and
   only becomes a real doom-stack if a layer lets players commit multiple nodes
   (team/squad RPS).
3. **[Systemic] Shallow ceiling + 33% tie rate.** Three nodes and no state means
   opponent-reading mastery caps fast (Koster's boredom threshold), and a third
   of throws are non-decisive.

*Economy, feedback loops, progression, difficulty curve: N/A — base RPS has
none.*

## 6. Improvement levers (smallest sufficient first)

1. **Iteration → best-of-N** (interaction-structure §2.1). Converts chance into
   pattern recognition — prediction shifts from "the optimal move" to "*this*
   player's bias." **Cost: ~zero** (same 3 options); this is why "best of 3"
   exists.
2. **Resource scarcity → a limited hand** (e.g., 3 Rock / 1 Paper / 1 Scissors)
   (§2.2). Adds state-dependent weighting and a memory/planning layer without new
   node types. **Cost: low-moderate** cognitive load (tracking spent throws).
3. **Disciplined roster expansion → 5-node (RPS-Lizard-Spock) or the 7-node
   2-Paradox** (§2.5). The 2-Paradox is the *exact* math fix for finding #2 — but
   only if you also add multi-node fielding. **Cost: cognitive load — stay ≤7
   nodes**; naive scaling to 15/25/101 keeps the math fair but *kills* the
   prediction loop under memorization overhead (Query 1).

## 7. Assumptions & open questions

- Base two-player single-throw RPS, symmetric fair play.
- If you mean an iterated/tournament format or a variant (RPSLS, 101-throw,
  hand-management), the diagnosis in findings #1–#3 shifts.

---

### Matrix diagnostics (raw)

```
Mode: binary | Nodes: 3 (Rock, Paper, Scissors)

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
  Paper: 0.3333
  Rock: 0.3333
  Scissors: 0.3333
```
