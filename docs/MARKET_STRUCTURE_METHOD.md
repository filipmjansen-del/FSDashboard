# Insurance Market Structure methodology

## Scope and source

This module measures the published F&P non-life market, segment **Skadeforsikring
i alt**, from `data/forsikring_market_structure_fp.csv`. The extract originates
from F&P's `kvartalsvise-markedsandele-1-2026.xlsx`, sheet *Skadeforsikring i alt*.
It is deliberately source-specific and is not merged into the financial-statement
workbook.

## Reported by F&P

- Gross premium income by market actor, in t.DKK.
- Market share by market actor. F&P's reported `market_share` is used directly
  and is **not recalculated by Databank**.

The share basis is **Bruttopræmieindtægter**. Market size is F&P's reported
period total, not a sum reconstructed by Databank.

## Calculated by Databank

For every year and quarter, Databank calculates rank, CR1, CR3, CR5, HHI and
the count of market actors with a positive reported market share. Rank and CR
metrics use descending F&P-reported shares. HHI is `10,000 × sum(s_i²)` using
those reported shares.

## Population, identity and time

The population follows F&P's published *Skadeforsikring i alt* population and
market-actor grouping. Source entity names are market actors/groups, not
necessarily individual legal entities. This is analytically different from the
`regnr` identity used for Databank financial-statement analysis; the dataset is
neither mapped to nor consolidated into that model.

Gross premium income is cumulative YTD. A selected Q2 is therefore compared
only with Q2 observations in earlier years; it is not compared with Q4 totals.
Missing source values remain missing and are never interpreted as zero.

## Validation

The source must have no duplicate year/quarter/entity-name rows, a single F&P
market total within each period, and reported shares reconciling approximately
to 100% per period.
