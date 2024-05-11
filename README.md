# CIFT
Caltech Intermediate Form parser in pure Python

## Under construction

Currently, CIFT is a utility for use in unit tests of RAIMAD,
a different project I am working on.
As such, it is only guaranteed to support CIF files that RAIMAD produces,
and not all CIF files in general.

Turning CIFT into a general-purpose CIF parser is a long-term future goal.

## Roadmap

- [ ] Basic parsing
    - [x] `P` (polygons)
    - [ ] `B` (box)
        - [ ] rotation
    - [ ] Comments
    - [x] Subroutines (`DS` and `DF`)
    - [x] Translation and rotation (subroutines)
- [ ] Inspection
    - [x] Get CIF file as a list of geometries on each layer
    - [ ] Get CIF file as a tree representing subroutine calls

## Overall Goals
- Pure Python, no dependencies
- easy to understand code
- `mypy --strict` has no complaints
- in abscence of a CIF spec,
emulate KLayout's CIF parser as closely as possible.

## Name
- "CIFT", pronounced like "sift".
Think of putting a CIF file into a sieve
and letting the syntax crystallize into grains of sand
that fall away to reveal the geometries it represents.

