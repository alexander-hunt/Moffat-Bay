# ADR 0004: Development room catalog overrides course rate table

- Status: Accepted
- Date: 2026-09-03
- Decision owner: Group B, led by Alexander Hunt

## Context

The course requirements specify four room configurations and rates: Double Full Beds at $120,
Queen at $135, Double Queen Beds at $150, and King at $160 per night. The original fictional
development seed data instead defines a lodge-specific room catalog with its own descriptions,
capacities, and nightly rates. The reservation workflow uses active `RoomType` records as its
authoritative catalog, so both data sets cannot describe the same implementation at once.

## Decision

Use the original `ROOM_TYPES` catalog in `moffat_bay/seeds.py` as the implementation's source of
truth. The active room types are Pinewood Studio at $145, Alder Suite at $195, Maple Cabin at
$245, and Douglas Fir Outpost at $495 per night.

This executive decision overrides the room configuration and nightly-rate table in the course
requirements for this implementation. Reservation forms, summaries, confirmations, lookup
results, development data, and tests must derive room information and pricing from `RoomType`.

## Consequences

- The application displays and books the four original lodge-specific room types rather than the
  course-table configurations.
- Server-side reservation pricing and capacity validation remains data-driven through `RoomType`.
- The idempotent seed test verifies the approved catalog and rates.
- Existing reservation seed records remain valid because their stored historical rates already
  match the original room catalog.
- Any future change to the approved catalog requires an update to the seed data, relevant tests,
  and this decision record or a superseding ADR.