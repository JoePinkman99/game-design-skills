
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

