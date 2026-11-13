---
summary: Five engineering guidelines for code written in this repo, each judged by a reviewer and enforced by no gate.
covers: [docs/design/**]
verified: 2026-11-12
verified_commit: 712486c
---
# Engineering standards

Code written in this repo follows five guidelines. Each is a guideline, not a gate. No tool checks any of them, and a reviewer judges each one while reviewing a change.

## Test-driven development

The test is written before the code it covers. A finished change does not show which came first, so a reviewer judges it by reading the change and asking the author.

## Unit tests use fakes

A unit test replaces everything outside its unit with a fake, so that it tests only what the unit is meant to do.

## Tests are weighed

The author considers the CPU time and the memory each test uses. Each test earns its place: its author can say what it proves that no other test proves. A test that duplicates another test's proof is removed.

## DRY and SOLID

Code avoids repeating knowledge. A fact, a rule, or a decision lives in one place, and other code refers to it.

Code follows the SOLID principles:

| Principle | Practice |
|---|---|
| Single responsibility | A unit has one reason to change. |
| Open/closed | A unit is extended without editing its working code. |
| Liskov substitution | A subtype stands in for its base type without breaking callers. |
| Interface segregation | A caller depends only on the methods it uses. |
| Dependency inversion | High-level code depends on abstractions, not on details. |

## Directories have one purpose

Every file in a directory serves the one purpose its name states. When that stops being true, the files are grouped into subdirectories. Two layouts are fixed and exempt: the docs tree, and the plugin's `agents` folder, where a subfolder would become part of an agent's name.

## How a reviewer applies them

- A reviewer reads each guideline as practice the author followed, and asks the author where the change is unclear.
- A departure from a guideline is raised in review and settled there.
