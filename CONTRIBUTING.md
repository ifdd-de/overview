# Contributing

`ifdd/overview` collects the descriptive side of `ifdd.de`: concepts, naming rules,
decisions. Code belongs in its own repository inside the `ifdd`
organisation and links back here.

## What fits here

- A new concept → `docs/concepts/NN-topic.md`
- A decision that closes an open question → `docs/decisions/NNNN-title.md`
- A correction to an existing document → a pull request against that file

## Conventions

- **Language:** English, including file names and headings.
- **Claims:** anything not verifiable from a linked source is marked `[VERIFY]`.
  Removing such a marker requires naming the source.
- **Decisions are append-only.** A superseded decision stays in place and gets a
  `Superseded by` line; it is not rewritten.
- **Identifiers never move.** Proposals that put an owner, an environment or a
  visibility class into a permanent IRI will be rejected — see
  `docs/concepts/02-namespace.md`.

## Decision records

Copy `docs/decisions/0000-template.md`, give it the next number, and open a pull
request. Status starts at `Proposed` and changes to `Accepted` when merged.

