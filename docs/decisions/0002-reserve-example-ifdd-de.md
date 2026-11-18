# 0002 — Reserve example.ifdd.de for examples

- **Status:** Proposed
- **Date:** 2026-11-13, amended 2026-11-17 (host names of the services of a demo node)

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
records. Demo nodes may get host names of the form `<node>.<domain>.example.ifdd.de`
(for instance `demo.grid.example.ifdd.de`), with generated data only. The services of
a demo node get host names one label below the node name,
`<service>.<node>.<domain>.example.ifdd.de` (for instance
`rest.demo.grid.example.ifdd.de`); that is four labels below `ifdd.de`, the most the
naming rules allow. Every host name has a record of its own. `example.ifdd.de` itself
redirects to <https://ifdd.de/example/>, which explains the namespace.

## Consequences

- Examples can use realistic names without the risk of meaning a real party.
- A name below `example.ifdd.de` is not necessarily a host: from the name alone, a
  reader cannot tell a context name from the host name of a demo node. The page
  <https://ifdd.de/example/> explains the difference.
- DNS stays simple: no wildcard record, only `example.ifdd.de` and single records
  for the services of demo nodes, about eight per node.
- A demo node is a public service under `ifdd.de`. It runs on a server of its own,
  holds generated data only and is rebuilt from scratch at regular intervals.
- The service host names depart from [concept 02](../concepts/02-namespace.md), which
  prefers services as paths. The demo follows the templates, which give every service
  a host name of its own (`wf`, for one, does not work below a path).
- The reservation rests on this decision only. Unlike `example.org`, which RFC 2606
  reserves, nothing outside this project enforces it.
