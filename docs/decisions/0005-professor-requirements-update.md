# ADR 0005: Professor requirements update

- Status: Accepted
- Date: 2026-09-09
- Decision owner: Group B, led by Alexander Hunt
- Supersedes: [ADR 0004](0004-development-room-catalog.md)

## Context

The professor has issued revised requirements for the lodge catalog and public website. The
application needs one authoritative set of current room rates, while historical reservation
records must retain the prices that were stored when those reservations were created. The public
information architecture also needs to consolidate contact information and add the approved
Salish Salmon image to the landing page.

## Decision

Apply a 5% increase to the four active room catalog rates established by ADR 0004. The active
`RoomType` catalog and all current reservation pricing must use these rates:

| Room type | Previous rate | Current nightly rate |
| --- | ---: | ---: |
| Pinewood Studio | $145.00 | $152.25 |
| Alder Suite | $195.00 | $204.75 |
| Maple Cabin | $245.00 | $257.25 |
| Douglas Fir Outpost | $495.00 | $519.75 |

The current `RoomType` catalog remains the source of truth for room names, descriptions,
capacities, availability, and nightly pricing. Historical reservation snapshots are not rewritten
when the catalog changes; their stored nightly rates and totals remain the values recorded at
confirmation time.

Remove the Contact Us page from the approved public-page set. The About Us page becomes the home
for the lodge's relevant contact information and must include approved address, telephone, and
email details. Exact contact values are not defined by this decision.

Use `archive/SalishSalmon.jpg` as the approved Salish Salmon image source for the landing page.
The later implementation must make the image available through the active static asset pipeline,
provide meaningful alternative text, and place it within the landing-page experience without
altering the source image in the archive.

## Consequences

- Reservation forms, summaries, confirmations, lookup results, development data, and tests must
  derive current room information and pricing from the updated `RoomType` catalog.
- Existing confirmed reservations retain their historical nightly rates and total costs.
- The public navigation and page set no longer include Contact Us.
- About Us must present the approved lodge contact information.
- The landing page includes the archived Salish Salmon asset through the active static asset
  pipeline with accessible alternative text.
- Implementing this decision will require coordinated follow-up changes to application data,
  templates, navigation, assets, and relevant tests. This ADR records the decision; it does not
  itself change those implementation files.