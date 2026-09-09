# ADR 0005: Professor requirements update

- Status: Accepted
- Date: 2026-09-09
- Decision owner: Group B, led by Alexander Hunt
- Supersedes: [ADR 0004](0004-development-room-catalog.md)

## Context

The professor has issued revised requirements for the application. All room rates need to be increased by 5%. The contact page should be removed and the relevant information should be presented on the About Us page. The Salish Salmon image needs to bee added to the landing page.

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
capacities, availability, and nightly pricing. 

Remove the Contact Us page. The About Us page becomes the home
for the lodge's relevant contact information and must include address, telephone, and
email details. 

Use `archive\SalishSalmonv2.png` as the source for the Salish Salmon image.

## Consequences

- Reservation forms, summaries, confirmations, lookup results, development data, and tests must
  derive current room information and pricing from the updated `RoomType` catalog.
- Existing confirmed reservations retain their historical nightly rates and total costs.
- The public navigation and page set no longer include Contact Us.
- About Us must present the approved lodge contact information.
- The landing page includes the archived Salish Salmon asset.