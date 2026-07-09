
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

