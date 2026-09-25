# 02 — Namespace: names as architecture

A DNS tree is a delegation tree. That makes it the cheapest available mechanism for
federation: handing someone a subdomain hands them autonomy, with cryptographic
signing and independent operation included.

## Three address spaces

| Purpose | Shape | Stability |
| --- | --- | --- |
| Vocabulary | `schema.<domain>.ifdd.de` | versioned, public |
| Identity | `id.ifdd.de/<domain>/<uuid>` | permanent |
| Location | `<node>.<domain>.ifdd.de` | operational, replaceable |

**The central rule: identifiers never encode an owner, an environment or a visibility
class.** All three change. A tool is sold, a service moves from private to public, a
node is rehosted — and every reference that encoded such a property breaks. A node
publishes its own current location as one of its attributes instead.

## Axes

| Axis | Meaning | Examples |
| --- | --- | --- |
| Domain | business area, delegation boundary | `tools`, `grid`, `lab` |
| Node | federation member inside a domain | `p1` … `p4` |
| Zone | visibility class, only when a domain mixes them | `private` |
| Service | endpoint role, preferably a path, not a label | `/api`, `/inventory.jsonld` |

Services are expressed as paths rather than labels so that one wildcard certificate
per domain is enough. Names stay at most four levels deep below `ifdd.de`.

## What a name does not do

- **`private` in a hostname is a label, not protection.** Access control comes from
  network segmentation, authentication and authorisation.
- **Hostnames are public.** Publicly issued TLS certificates appear in Certificate
  Transparency logs, so any certified hostname is discoverable. Use a wildcard, an
  internal CA or split-horizon DNS where that matters.
- **Pseudonyms cost nothing.** Nodes are named `p1`, not by person.
