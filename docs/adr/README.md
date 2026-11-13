# ADRs

Each ADR records one decision that is costly to reverse. Read the ADR for an area before changing it.

- [0001-architecture.md](0001-architecture.md): Avalon is a plugin of three layers with a standard-library Python script that never calls a model, has a pure core and all-or-nothing writes, and reads git through one read-only module.
- [0002-documentation-system.md](0002-documentation-system.md): This repo uses Avalon for its laws, ADRs, and design docs, with the root at docs/.
