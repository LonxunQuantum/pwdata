# Electrolyte Fragment Charge Preprocessing Design

## Scope

Implement a preprocessing pipeline for
`/data/public/wuxingxing/electrolytes/decompress/0-19/part000.xyz`.
Production code lives under `pwdata/electrolytes/`. Results are written to
`/data/public/wuxingxing/electrolytes/decompress/datacout/part000`.

The source file contains 1675 neutral frames with 148 to 3068 atoms per frame.
Its atom properties are `species`, `pos`, and `forces`; it has no frame charge
field, so the configured frame target charge defaults to zero.

## Output Semantics

The annotated extended XYZ preserves every source field and adds:

- `fragment:I:1`: a zero-based fragment identifier local to the frame.
- `charge:R:1`: the target total charge of that fragment, repeated on every
  atom belonging to the fragment.

Training code must group atoms by `fragment`, sum predicted atomic charges in
the group, and compare that sum with one deduplicated `charge` label. It must
not sum the repeated labels. An unresolved fragment is written with `charge=nan`.

## Fragment Construction

Each frame is streamed from extended XYZ. Covalent bonds are found with a
periodic neighbor list and a general 3x3 cell; no all-atom distance matrix is
constructed. Candidate bonds use configurable element-pair cutoffs derived
from covalent radii, plus element valence limits. Hydrogen and halogen atoms
have maximum covalent degree one. Over-valent or equal-quality competing
assignments are reported as ambiguous.

Li, Na, K, Mg, Ca, Fe, and Zn never participate in the covalent fragment graph.
They remain single-atom fragments even when short coordination contacts exist.
Connected components are obtained with union-find. Every atom must occur in
exactly one component.

## Fragment Signatures

Fragment identity does not depend on atom order or a species name. A stable
signature combines:

- Hill-style formula;
- element-labelled Weisfeiler-Lehman topology hash;
- node-degree histogram;
- element-pair edge counts.

The catalog retains the unhashed invariants as a collision guard. Signatures
with incompatible invariants are reported instead of merged.

## Charge Resolution

Charge resolution follows a strict precedence order:

1. Exact signature assignments in a human-editable YAML registry.
2. Deterministic rules for validated fragments. Monatomic Li, Na, and K are
   +1; Mg and Ca are +2; monatomic F, Cl, Br, and I are -1. The initial
   topology-checked registry covers H2O (0), DMF (0), SO4 (-2), TFSI (-1),
   FSI (-1), BF4 (-1), PF6 (-1), DMSO (0), and DMSO2 (0). A matching formula
   without the registered topology is not assigned automatically.
3. Dataset-level neutrality equations for all frames without Fe or Zn:
   `sum(fragment_count * signature_charge) = frame_target_charge`.

Inference first propagates equations containing one unknown signature, then
solves each remaining full-rank connected equation system. A solution is
accepted only when it is unique, integral, within the configured range -4 to
+4, and exactly satisfies every participating frame. Underdetermined,
non-integral, or conflicting systems remain unresolved. Heuristics and priors
may rank a report but may not create a charge label.

After all non-Fe/Zn fragment charges in a frame are known, Fe and Zn are
resolved by conservation. A single Fe receives the remaining frame charge.
For Zn, the remaining total charge is divided equally among all Zn fragments.
Frames containing both Fe and Zn, multiple Fe atoms, or an unknown nonmetal
fragment remain unresolved and are reported.

## Components

- `pwdata/electrolytes/extxyz_io.py`: streaming parser and annotated writer.
- `pwdata/electrolytes/fragment_graph.py`: periodic neighbor search,
  valence-aware bond selection, and union-find components.
- `pwdata/electrolytes/signatures.py`: formula and order-independent topology
  signatures.
- `pwdata/electrolytes/charge_inference.py`: registry, rules, neutrality
  equations, Fe/Zn residual handling, and validation.
- `pwdata/electrolytes/preprocess.py`: two-pass CLI orchestration and reports.
- `pwdata/electrolytes/fragment_charges.yaml`: validated seed assignments and
  inference limits.
- `tests/electrolytes/`: focused graph, signature, inference, I/O, and Zn
  regression tests.

The first pass builds fragments and a signature catalog for all frames. The
second pass resolves charges, validates neutrality, and writes the annotated
XYZ and reports.

## Results

The output directory contains:

- `part000_fragment_charge.xyz`;
- `fragment_signature_catalog.tsv`;
- `frame_charge_summary.tsv`;
- `charge_inference_report.tsv`;
- `unresolved_fragments.jsonl`;
- `fragment_charge_summary.txt`;
- `fragment_charge_metadata.npz`.

Reports include source path, SHA-256, size, and modification time. The summary
records resolved and unresolved frame counts, signature counts, neutrality
violations, Fe/Zn charge distributions, and atom-assignment validation.

## Verification

Automated tests cover general-cell periodic bonds, atom reordering, metal
isolation, hydrogen-bond rejection, signature stability, unique and
underdetermined charge systems, Fe/Zn conservation, repeated charge-column
semantics, streaming I/O, and unknown/ambiguous reporting. The existing
`Zn.xyz` regression must still produce 67 H2O, 23 DMF, 7 SO4, 7 Zn, Zn total
charge +14, and Zn average charge +2.

The complete `part000.xyz` run is accepted only if every atom receives exactly
one fragment ID, every resolved frame has a unique fragment charge per group,
and the deduplicated fragment charges sum to zero within `1e-8`.
