# History

IFDD is the current name for a line of work that has been running for years, always
circling the same question: **how do you keep distributed systems describable without
forcing them into one system?**

This page is for readers who want to know which parts are new and which parts have
already been built once.

---

## d3 — distributed data driven

**d3** — short for **distributed data driven**. Four Python components, BSD-3-Clause,
built around 2020. The name already contains the thesis: data is distributed, and the
system is driven by that fact rather than fighting it.

| Component | Role |
| --- | --- |
| `d3context` | JSON-LD contexts, served as their own containerised service |
| `d3ct` | core tools — a plugin pipeline that collects, transforms and emits |
| `d3api` | REST API over the collected graph |
| `d3ui` | web front end on top of that API |

### What d3 already got right

- **Vocabulary as a deployable artefact.** `d3context` ships roughly 35 JSON-LD
  contexts — data centre items, hosts, VMs, Kubernetes, network, invoices, users — as
  a standalone nginx container. The context has its own address, separate from any
  application. IFDD's `schema.<domain>.ifdd.de` is the same move.
- **Temporal validity in the vocabulary.** Every context carries `validNotBefore` and
  `validNotAfter` alongside `created`, `modified` and `expire`. Time was a property of
  the statement, not an afterthought.
- **Provenance in the vocabulary.** `origin` and `publisher` are part of the base
  vocabulary, so a record can say where it came from.
- **Collect, do not copy.** `d3ct` reads from the systems that already own the data —
  vSphere via `pyvmomi`, directories via `python-ldap`, HTTP sources with a request
  cache — and composes them in a pipeline of small plugins.
- **Federated identifiers.** `trans_uuid` mints UUIDv4 during the transformation, with
  no central allocator. IFDD still does exactly this.
- **Aspects and tags.** Items carry an `aspect` and a `tags` set, the beginning of the
  faceted description IFDD now models explicitly.

### Where it reached its limits

- **Contexts were handwritten.** Thirty-five JSON-LD files, maintained by hand, with
  term IRIs pointing at `http://localhost:8811/...` — development addresses that never
  became stable identifiers. IFDD answers this with a generated context and a
  permanent identifier space under `id.ifdd.de`.
- **No schema, only a context.** JSON-LD gives meaning but not structure. Nothing
  validated that a record was complete or well typed. LinkML closes that gap.
- **The pipeline was the product.** Integration happened inside `d3ct` at collection
  time; the sources themselves stayed mute. IFDD pushes the contract outwards, so a
  source publishes conformant data itself and the aggregator becomes replaceable.
- **One graph, one operator.** `d3api` held the assembled graph in memory with
  `networkx`, behind one JWT-protected API. That is a central system with distributed
  inputs — federation of data, not yet federation of responsibility.

## d4 — the template generation

**d4** is a cookiecutter template for Python microservices. A generated service collects data from one or more
single points of truth and republishes it as JSON-LD over REST — again without copying
it into a central store.

Two lessons came out of that phase:

- **Scaffolding works, but only for scaffolding.** Everything identical across all
  instances belongs in an installable library, not in a template. Templates stay dumb:
  names, wiring, CI.
- **The interesting part was never the service.** It was the contract the services
  agreed on. That observation is what turned a template into an architecture.

## What IFDD adds

| Carried over from d3 and d4 | New in IFDD |
| --- | --- |
| Distributed data as the default | A namespace that encodes the federation in DNS |
| JSON-LD contexts as their own service | A LinkML schema as a validated contract, context generated from it |
| Temporal validity and provenance as first-class terms | Identity separated from location and from ownership |
| Decentralised UUID minting | Identifiers under a permanent domain instead of localhost URLs |
| Collecting instead of copying | Sources publish conformant data themselves |
| Open source, permissive licence | A public reference case anyone can reproduce |

## Reading this page

Nothing here is load-bearing for the current work — it is context, not authority. The
d3 statements above are taken from the source archives of the four components. The
components themselves are not part of IFDD and are described here for background only.
