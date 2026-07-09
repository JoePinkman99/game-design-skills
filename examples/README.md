# Examples — three real runs, unedited

Everything in this folder is raw skill output. Nothing was cleaned up for
publication; a few claims even turned out to be tool bugs, which is how the
script gained its signed-matrix guard. Each folder is numbered in loop order:

```
01-audit.md          game-analysis on the original game
02-redesign.md       game-redesign consuming that audit
03-handoff-spec.md   the recommended proposal as a self-contained spec
04-blind-reaudit.md  game-analysis again — fresh session, zero memory of the design rationale
```

## rock-paper-scissors/ — the full loop on the simplest possible game

What to look for:

- **01** correctly refuses to treat the "all pairs unbeatable" script finding
  as a flaw — you throw one sign per round, so there is no stacking layer for
  a doom-stack to live in. Knowing when the math *doesn't* bite is half the
  discipline.
- **02** proposes three redesigns, including **Sharpened Throws** (weighted
  win values 1/2/3 + a tie pot) with a hand-derived Nash equilibrium
  (Rock ½, Paper ⅙, Scissors ⅓), and a 7-sign expansion built on the
  proven-minimal "2-Paradox" tournament — with the classic trio embedded
  unchanged and the historically banned **Well** as its hook.
- **04** is the payoff: a blind session independently re-derives the same
  equilibrium, solves the full match by backward induction (200k-match
  simulation included), confirms every structural claim — and finds a real
  issue the designer missed: a player using classic-RPS habits loses
  **0.817 : 0.183** to plain arithmetic, with nothing in the rules signaling
  why. Its strongest recommendation: change nothing mechanical, fix it with
  two printed sentences.

## hex-crawler/ — the loop on an original tactics design

What to look for:

- **01** catches the source design's own doom-stack story leaning on spatial
  reasoning its matchup chart doesn't support — and shows the deeper fact:
  in the 4-unit game, *every* army pairing was mathematically void
  (all disjoint matchups sum to exactly zero; only positioning ever decided
  anything).
- **02** delivers the **War Wheel**: a 7-unit chart where every pair of units
  has a counter (script-verified: `size 2: none — the 2-Paradox property
  holds.`), the legacy four units keep all their old matchups, plus a
  simultaneous-orders wildcard and a three-objective Blotto-style pivot where
  the script proves all-in stacking is a *dominated* plan.
- **04** independently proves the proposed chart is the **unique** valid
  7-node solution (one isomorphism class out of 2,097,152 tournaments — any
  edge flip destroys the property), then finds the design's real hole:
  nothing in the rules ever *forces* an engagement, so a faster army can
  refuse to lose forever. Its proposed fix independently re-derives the
  objectives idea from 02 — two blind sessions converging on the same
  mechanism.

## tetris/ — knowing when the matrix is the wrong tool

A single audit, included as the negative-space example: Tetris has no
piece-vs-piece interaction chart, and the skill says so instead of forcing
one — the whole analysis runs on the fun-engine and systemic-lever modules
(the inverted economy: the game faucets terrain *at* you, line clears are the
only drain, and the faucet always wins — Tetris is designed to be lost).
