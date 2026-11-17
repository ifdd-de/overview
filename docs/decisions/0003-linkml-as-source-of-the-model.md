# 0003 — LinkML as the source of contexts, vocabularies and units

- **Status:** Proposed
- **Date:** 2026-11-14

## Context

The JSON-LD contexts of the `schema` service, the vocabularies of the `type`
service and the units of the `unit` service describe the same terms from three
sides: IRI and coercion, labels and order, units and quantity kinds. They were
written by hand in three repositories, so every term was maintained in up to
three places, and nothing checked that they agreed.

## Decision

Each namespace is described once, in a LinkML file. A build generates the
context, the vocabulary or the units and a documentation of the namespace from
it. The template `ifdd-de/model` holds the build and the example namespaces; an
instance is the model repository of an installation and copies the generated
files into the content repositories of `schema`, `type` and `unit`.

- One standalone LinkML file per namespace. Terms every context needs
  (`objType`, `objName`, `origin`, `publisher`, the `c_*` terms) are written
  out in each file, because each context defines them in its own namespace.
- The context comes from LinkML's `gen-jsonld-context` plus a post-processing
  step: it removes `@vocab`, so that undefined terms stay undefined, removes
  class terms and adds the header of an IFDD context.
- Generated files are compared by meaning (JSON-LD processing, canonical
  N-Quads) with reference files before they are published.

## Consequences

- Labels, comments, order and units are edited in one file per namespace.
- The build depends on LinkML, PyLD and, for the diagrams of the
  documentation, PlantUML with Java and Graphviz.
- The hand-written example files in `ifdd-de/schema`, `ifdd-de/type` and
  `ifdd-de/unit` become generated files; the templates keep them as examples.
- Status *Proposed* until the model template is published and used by an
  installation.
