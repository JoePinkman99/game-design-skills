# Game Analysis Report — Hex-Crawler Tactical Combat Loop

*Subject: the tactical combat loop specified in [analysis-workflow.md §2](game-analysis/references/analysis-workflow.md) ("End-to-End Worked Example: The Hex Crawler Strategy Game"), analyzed as a submitted design.*

> **Framing note.** I treat §2's four-unit combat loop as the *current* design and §2's Step 6 items (7-node expansion, fog of war, action economy) as *proposed* fixes, not shipped mechanics. §3 of that file already carries a methodological note on the example; I ran the analysis independently and cross-check against it in §5 rather than restating it.

---

## 1. Game snapshot

- **Working name:** Hex-Crawler Tactical Combat Loop (HoMM-inspired turn-based strategy).
- **Intake path:** B — read-and-extract from provided material (the node set and interaction edges are stated explicitly in §2, Steps 1–2).
- **Material examined:** `analysis-workflow.md` §2 (Steps 1–6) and §3 (methodological note).
- **Confidence:** High on the interaction core — the four nodes and all six matchups are fully specified, so the matrix is exact, not reconstructed. Low on everything *around* the core — stats, HP/damage, recruitment economy, movement-point values, and whether information is hidden are all unspecified or named only as proposed levers. Findings are therefore split cleanly between the **[Matrix]** layer (certain) and declared **[Spatial]/[Information]/[Systemic]** layers (conditional on assumptions in §7).

---

## 2. Typology

| Axis | Verdict | Evidence |
|------|---------|----------|
| Transitive / intransitive | **Intransitive** | `matrix_analysis.py`: `INTRANSITIVE (cycle exists). Example cycle: Infantry -> Pikemen -> Cavalry -> Ranged -> Infantry`. Note **zero 3-cycles** — the loop is a single 4-cycle, not a stack of RPS triangles (interaction-structure.md §3.1). |
| Simultaneous / sequential | **Sequential** | Turn-based hex crawler (§2, Step 4). No concurrent resolution — the "Simultaneous Action / Zero-Reactivity" pillar (interaction-structure.md §1.2) is *absent*. |
| Symmetric / asymmetric | **Symmetric (roster)** | Both sides draw the same four archetypes; viability is uniform (0.2500 each, below). The design's own "slightly asymmetrical" (§2, Step 3) conflates roster asymmetry with matrix *sparseness* — see next row. |
| Spatial / abstract | **Spatial** | Hex grid, flanking, maneuver, movement points (interaction-structure.md §2.3). |
| Dense / sparse matrix | **Sparse** | Not a tournament: `Tournament: no`. Two of six matchups are neutral (Infantry–Cavalry, Ranged–Pikemen). |

**Genre framing implied:** a *sequential, spatial, symmetric positional-tactics wargame* built on a thin intransitive core — the Fire Emblem / Total War / HoMM lineage, where an RPS counter-web is meant to be enriched by grid maneuver. The typology's tension is immediate: a **sparse 4-node core** carries almost no counterplay on its own, so the entire prediction burden is offloaded onto the spatial layer. §5 shows that offload doesn't hold.

---

## 3. Systems map

**Core loop (bullet chain):**
- Observe the enemy army on the grid → compose / position your own units →
- maneuver over several turns to force favorable matchups (land your counter-unit onto their unit) while denying them the mirror →
- resolve combats → attrition → repeat until one army breaks.

**Node set:** `{ Infantry, Cavalry, Ranged, Pikemen }` — stripped of stats per §2, Step 1.

**Interaction matrix** (row's result vs column; W = row wins, L = row loses, N = neutral):

|  | Infantry | Cavalry | Ranged | Pikemen |
|---|:---:|:---:|:---:|:---:|
| **Infantry** | — | N | L | **W** |
| **Cavalry** | N | — | **W** | L |
| **Ranged** | **W** | L | — | N |
| **Pikemen** | L | **W** | N | — |

Each unit beats exactly one other, loses to exactly one, and is neutral with one. This regularity is why viability is perfectly flat and — as §5 shows — why *every* pair is unbeatable.

**Economy flows:** *Largely unspecified.* No faucets/sinks are given (Machinations vocabulary, systemic-levers.md). The only resource-shaped mechanic named is **movement points**, and it appears only as a *proposed* lever (§2, Step 6), not as confirmed current design. Treated as an assumption (§7).

**Progression gates:** None in the current loop. Act-based escalation (1 element → 3-node → 7-node) is a *proposed* lever (interaction-structure.md §2.5), not present.

---

## 4. Fun engines

Ranked by how much play time each plausibly explains.

1. **Prediction loop (spatial variant)** — *framework:* interaction-structure.md §1; fun-engines.md. *Evidence:* the intransitive counter-web + "predict how the enemy maneuvers over the next three turns" (§2, Step 4). *Sustains:* a balanced intransitive network read through positioning. *Kills:* a solved matrix; broken simultaneity. *Health:* **broken** — the engine's two structural supports are both failing here: simultaneity is absent by genre (sequential), and the matrix is trivially solvable by 2-stacking (§5, Finding 1). What remains is spatial calculation, not opponent-reading.

2. **Pattern mastery** — *framework:* Koster, *A Theory of Fun* (fun-engines.md). *Evidence:* learning which unit answers which, and which formations counter which. *Sustains:* fresh interactions at the edge of competence. *Kills:* solved patterns. *Health:* **at risk → broken** — with only 4 nodes and a universal invincible pair, the pattern space is tiny and exhausts quickly; mastery arrives, then boredom.

3. **Challenge** — *framework:* MDA (Hunicke, LeBlanc & Zubek). *Evidence:* win/loss tactical combat with a skill ceiling. *Sustains:* opponents who can't be beaten by rote. *Kills:* a dominant strategy. *Health:* **at risk** — real while the doom-stack is undiscovered; collapses the moment a player finds it (which the matrix says is immediate).

*Also present, threatened:* **Self-determination / autonomy** (Ryan & Deci, fun-engines.md) — HoMM-likes sell viable army-composition variety. The universal doom-stack makes that choice partly illusory (one class of build dominates), which is precisely the autonomy kill condition ("one true build").

---

## 5. Diagnosis

Severity-ordered. Matrix findings cite `matrix_analysis.py` verbatim.

### Finding 1 — [Matrix] **Every unit pair is an invincible "doom-stack." — Critical**

```
== DOOM-STACKS (unbeatable subsets) ==
6 unbeatable subset(s) of size 2 — 2-Paradox property does NOT hold:
  ('Infantry', 'Cavalry')
  ('Infantry', 'Ranged')
  ('Infantry', 'Pikemen')
  ('Cavalry', 'Ranged')
  ('Cavalry', 'Pikemen')
  ('Ranged', 'Pikemen')
```

Because each unit beats *exactly one* other unit, no single unit can beat *two* units at once — so **no** pair has a clean counter. The design's Step 5 named only **Cavalry + Ranged**; the matrix shows the pathology is universal and structural, not specific to that combo. Any two archetypes fielded together are unanswerable at the matrix layer. This is the interaction core being solved on turn one. **Root cause:** the sparse 4-node structure itself — a 2-Paradox (every pair has a counter) provably requires **≥ 7 nodes** (interaction-structure.md §2.5, Query 4).

### Finding 2 — [Matrix] **Sparse, tie-heavy core with a tiny option pool. — High**

`Tournament: no` — two of six matchups (Infantry–Cavalry, Ranged–Pikemen) are neutral. Neutral matchups let a player *opt out of the mind-game entirely* by locking into a no-counterplay engagement (the design flags this approvingly in Step 3; it is actually a defect for a prediction game). Combined with only four nodes, the learnable interaction space is minuscule and solves fast — feeding the Finding 1 collapse and the Pattern-mastery kill condition (§4). Cognitive load is comfortably low (good), but so is depth.

### Finding 3 — [Information] **Perfect information under sequential turns degrades prediction into calculation. — High**

The prediction pillar requires either simultaneity or hidden information (interaction-structure.md §1.2; systemic-levers.md, "Hidden information"). This loop is sequential *and* — as specified — fully observable (you "look at the enemy army on the grid"). With visible state and a solvable matrix, the "predict their maneuver over three turns" claim reduces to computing the opponent's optimal move, not reading a mind. The spatial layer alone cannot supply a prediction burden the information structure has already removed.

### Finding 4 — [Spatial] **The design's own doom-stack narrative leans on an undeclared spatial layer, misdiagnosing the cause. — Medium**

Step 5 justifies Cavalry + Ranged with: "the Cavalry protects the Archers from Infantry, and the Archers shoot down the Pikemen." Against the **pure matrix**, both halves are false: Ranged already **beats** Infantry (no protection needed), and Ranged–Pikemen is **neutral** (archers don't beat pikemen). The story is a *spatial* one (screening, standoff range) layered over a matrix fact that is simpler and worse — *all* pairs are unbeatable. Diagnosing through the narrative understates severity and points at a unit-specific fix when the real problem is the 4-node structure. (This independently reproduces standing rule 1 and the §3 methodological note.)

### Finding 5 — [Systemic] **The proposed 7-node fix pushes cognitive load toward its ceiling. — Low/Medium**

Expanding to a 7-node 2-Paradox is the correct structural fix (Finding 1), but it raises the pairwise interactions a player must hold from **6 → 21** unordered matchups, plus three new unit identities. That is near the upper edge of the "low cognitive load" pillar; hyper-scaling the option pool destroys the prediction loop (interaction-structure.md Query 1 / standing rule 4). Not a defect in the current loop — a caution on how to introduce the fix.

---

## 6. Improvement levers

Smallest sufficient lever per finding; predicted effect; risk/cost incl. cognitive-load delta. **Ordering matters:** only the first lever removes the root pathology — the rest enrich the spatial/information layers but *mask* a solved matrix rather than solving it.

### Lever A (primary, load-bearing) — Math: expand to a 7-node 2-Paradox
*Fixes Findings 1 & 2.* Introduce three nodes (e.g. Magic, Flying, Siege) and wire the win/loss edges so **every** two-node subset has at least one counter (interaction-structure.md §2.5).
- **Predicted effect:** no invincible composition; the board can no longer be statically solved; the prediction and pattern engines are restored to health.
- **Why this is the *smallest* sufficient lever:** a cheaper alternative — filling the two neutral edges to make a 4-node *tournament* — removes tie-hiding (Finding 2) but **not** the doom-stack: the 2-Paradox property is impossible below 7 nodes (Query 4). So 7 nodes is the provable floor for "no invincible pair."
- **Risk/cost:** cognitive load **6 → 21** pairwise matchups (Finding 5). Mitigate with **act-based subsetting** (Lever D). Careless edge-wiring can reintroduce dominated nodes or new doom-stacks — **re-run `matrix_analysis.py --max-stack 2` on the proposed 7-node chart before shipping** and confirm `2-Paradox property holds` and `Dominated nodes: none`.

### Lever B (complement) — Information: fog of war / hidden composition
*Addresses Finding 3.* Hide enemy composition and position; force scouting.
- **Predicted effect:** restores a prediction burden in a sequential game — the substitute for simultaneity (systemic-levers.md, "Hidden information").
- **Risk/cost:** over-hiding turns decisions into coin flips and makes scouting a mandatory chore (same source). **Does not fix the matrix** — a hidden invincible pair is still invincible once revealed; fog only delays the solve. Complement to Lever A, never a substitute.

### Lever C (complement) — Resource: action economy / movement points
*Addresses the execution side of Finding 3.* Limit movement points so the right counter-unit can't always reach the target hex in time.
- **Predicted effect:** keeps positioning and turn-sequencing live decisions (interaction-structure.md §2.2; systemic-levers.md, pacing).
- **Risk/cost:** too tight → fiddly micro. Again masks rather than fixes the matrix.

### Lever D (enabling) — Escalation scaling: subset the roster by act
*Mitigates Finding 5.* Ramp 1 element → 3-node triangle → full 7-node 2-Paradox across acts (interaction-structure.md §2.5).
- **Predicted effect:** cognitive load grows with player mastery instead of arriving all at once.
- **Risk/cost:** low; mainly content-pacing work.

### Lever E (process guardrail) — Matrix-first diagnosis
*Addresses Finding 4.* Before attributing any matchup outcome to terrain/range/screening, verify it against the pure matrix; re-run the script on any new chart.
- **Predicted effect:** prevents spatial narratives from hiding structural defects (standing rule 1).
- **Risk/cost:** none — a discipline, not a mechanic.

---

## 7. Assumptions & open questions

- **No stat layer.** Per Step 1 the nodes are stripped of HP/damage/movement. Real balance depends on stats not given; all findings are about the *archetype counter-web*, and a stat layer could distort the flat 0.25 viability.
- **Perfect information is inferred**, from "looking at the enemy army on the grid." Fog of war is explicitly a *proposed* lever, so the base design is treated as fully observable. If the base game already hides information, Finding 3 softens.
- **Symmetric roster is inferred** from the HoMM framing (both sides field the same archetypes). If factions had disjoint rosters, the game shifts toward an asymmetric knowledge-check (interaction-structure.md §2.4).
- **Economy is unspecified.** Movement points are treated as a proposed lever, not confirmed current mechanic; no faucets/sinks are defined.
- **The 7-node expansion's edge wiring is not given**, so I cannot verify it actually achieves a 2-Paradox — it must be matrix-tested when defined (Lever A risk note).
- **Out of scope:** the strategic/campaign layer above tactical combat (recruitment, map objectives), audiovisual/sensation engines, and multiplayer/fellowship dynamics — none are described in §2.

---

*Method: game-analysis skill, 8-step procedure. Matrix diagnostics: `game-analysis/scripts/matrix_analysis.py` on a 4-node binary matrix (`Infantry, Cavalry, Ranged, Pikemen`). Framework claims attributed inline to `interaction-structure.md`, `fun-engines.md`, and `systemic-levers.md`.*
