# 0002 — Reserve example.ifdd.de for examples

- **Status:** Proposed
- **Date:** 2026-11-13

## Context

Documentation, templates and test data need names that look like real IFDD names —
context names, client patterns, host names — without naming a real organisation or
system. They already use the fictional organisation `example` with the domains `grid`
and `ops`, for instance the context names `breaker.grid.example.ifdd.de` and
`maintenance.ops.example.ifdd.de`. Readers who look such a name up find nothing, and
no document says why. Demo nodes may later need real host names in the same tree.

## Decision

`example.ifdd.de` and every name below it are reserved for examples. No real
organisation, domain or data is placed there. Context names below it never get DNS
records. Demo nodes may get host names of the form `<node>.grid.example.ifdd.de`, each
with a record of its own and with generated data only. `example.ifdd.de` itself
redirects to <https://ifdd.de/example/>, which explains the namespace.

## Consequences

- Examples can use realistic names without the risk of meaning a real party.
- A name below `example.ifdd.de` is not necessarily a host: from the name alone, a
  reader cannot tell a context name from the host name of a demo node. The page
  <https://ifdd.de/example/> explains the difference.
- DNS stays simple: no wildcard record, only `example.ifdd.de` and, if they ever
  exist, single demo hosts.
- The reservation rests on this decision only. Unlike `example.org`, which RFC 2606
  reserves, nothing outside this project enforces it.
