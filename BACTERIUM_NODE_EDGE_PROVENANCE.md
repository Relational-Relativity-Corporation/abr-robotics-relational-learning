# ORIGIN DECLARATION — Bacterium nodes, edges, and observable provenance

**Status:** Origin-directed proposed field inventory for Claude to implement; physical observations and mathematical edge admissibility must be reported honestly.  
**Authority:** canonical abr-kernel V9 through abr-relational-processor; no IRRS, new operator mathematics, or validation framework.

## Governing organization

**The organism is one relational field. Its memory is its genetics.** Genetic memory is a constituent node of the organism, not a bookkeeping object outside the field. The inherited genetic state establishes receptor configuration, retention, relational-processing organization, body, and response policy. Its first actual sensory measurement is implanted into that memory **before** the behavior loop; this does not manufacture an earlier observation. The organism's full A/B/R and applicable derived/persistence architecture exists from the first field declaration. An operator may remain unevaluated only when its canonical requirements are not satisfied.

**Important provenance distinction:** An inherited configuration or software record is observable as such, but is not automatically evidence of a biological gene, physical motor motion, or a numerically admissible kernel edge. Record these distinctions as data, not as reasons to omit nodes.

## Nodes — include every constituent, record its source

| ID | Node | Observable value/state | Source and provenance | Measurement/role |
|---|---|---|---|---|
| G | Genetic memory | Inherited receptor geometry, memory/write/read rules, operator invocation specification, P-1 policy, declared parameters; retained first reading and subsequent episodes | Exact genetic declaration file hash/version; memory write/read event IDs; source frame hash for each stored reading | Config and retained observation; do not disguise config values as DN |
| S_L | Left receptor | Actual green-channel intensity at x−16 on declared image row | Camera frame hash, timestamp semantics, pixel coordinate, raw channel DN | DN, sensor observation |
| S_C | Center receptor | Actual green-channel intensity at x on declared image row | Same camera frame identity, own coordinate and DN | DN, sensor observation |
| S_R | Right receptor | Actual green-channel intensity at x+16 on declared image row | Same camera frame identity, own coordinate and DN | DN, sensor observation |
| P | Relational processing | Exact submitted field, kernel invocation, operator outputs and kernel commit | Processor declaration/output IDs and kernel source revision | Computed states, not raw physical readings |
| B | Body / sampling position | Current selected image-column coordinate, body orientation declaration, boundary and step setting | Program state/command log; subsequent camera request coordinate | px, software state; not independently measured physical displacement |
| M | Motor/actuation interface | Direction decision, commanded next sampling coordinate, blocked condition | Declared P-1 rule, operator-output ID, command event | Command, not observed motor torque or displacement |
| E | Environment interaction | Subsequent camera frame and receptor readings at selected coordinate | Acquisition record/frame hash | Measured response; cause of light variation remains OPEN |

Node identities are conceptual roles; do not coerce heterogeneous quantities into one DN-valued field. Where the processor requires a homogeneous numerical basis, create a compatible **observed subfield** without deleting G, P, B, M, or E from the organism's declared organization.

## Edges — declare provenance and separate relationship from admissibility

| ID | From → to | Relationship and direction basis | Observable provenance | Mathematical status |
|---|---|---|---|---|
| e1 | S_L → S_C | Left-to-center in explicitly declared body-oriented receptor geometry; orientation is a **genetic convention** unless independently measured | Sensor geometry declaration; coordinates in the same hashed frame; actual DN readings | Candidate spatial edge; check kernel admissibility and whether declared direction suffices |
| e2 | S_C → S_R | Center-to-right in same body-oriented geometry | Same-frame coordinates, DN, geometry declaration | Candidate spatial edge; check kernel admissibility |
| e3 | S_L/S_C/S_R → G | Sensory readings written to genetic memory | Actual frame IDs, write event IDs, stored values | Observable data-flow; not automatically kernel spatial edge |
| e4 | G → P | Retained observations and inherited configuration supplied for calculation | Memory retrieval event, source observation IDs, exact processor input | Observable data-flow; do not substitute for kernel persistence |
| e5 | S_L/S_C/S_R → P | Current sensory field submitted to canonical processor | Submitted field JSON and matching acquisition records | Kernel input provenance |
| e6 | P → M | Declared policy consumes specified canonical output and emits command | Exact operator output, P-1 rule version, command event | Observable computational/command relation; choice of output OPEN |
| e7 | M → B | Command updates the sampling coordinate or is blocked | Command log and resulting program state | Software actuation; not physical motion |
| e8 | B → S_L/S_C/S_R | Current coordinate determines next actual camera sample sites | Next camera request, frame hash, coordinates and readings | Acquisition coupling; physical causality of brightness OPEN |
| e9 | P(k) → P(k+1) | Canonical temporal continuation/persistence across actual successive field observations | Retained prior canonical output, current declaration, ordered acquisition records | Canonical persistence only; not a fabricated spatial edge |
| e10 | G(k) → G(k+1) | Genetic memory retains episode and updates stored observation | Memory read/write records with source frame and prior episode ID | Recorded state transition; do not conflate with e9 |

## Startup and execution

1. Instantiate **all nodes and declared relations** from genetic organization before behavior starts. Record configuration and provenance; unavailable measurements remain unavailable, not invented.
2. Acquire a real first frame, record all three receptor values and implant the measurement/episode into G. Record actual write and optional read-back events.
3. Submit the admitted same-frame numerical subfield to the canonical processor. Evaluate all eligible A/B/R/ρ and other canonical outputs immediately; **R is not disallowed merely because this is k0**. If the spatial topology or direction is inadmissible, report the specific missing declaration.
4. Save the first canonical output in genetic memory. On the next real frame, evaluate all eligible current-field operators plus persistence with the actual retained kernel state.
5. Only after source-backed mathematical review, enable P-1 and the behavioral loop; the policy input must be explicitly selected from the new canonical outputs.
6. For each step, preserve current raw observation, memory provenance, exact kernel declaration/output, command, subsequent observed sampling coordinate and reading. Report what is observed, calculated, commanded, and OPEN.

## Claude instructions and stop point

Read this file, `ORIGIN_BACTERIUM_RESET.md`, and actual kernel/processor source. Update `PHASE0_1_FOUNDATION_PROPOSAL.md` to **include genetic memory G as a node** and the above complete inventory. Audit e1/e2 direction against the canonical requirements; do not silently declare software array order to be a physical direction. Audit the numeric admissibility of each edge rather than deleting it from the organism's organizational graph. Identify the minimal homogeneous subfield where R is actually evaluable.

**Stop and return** the corrected node/edge provenance table, exact canonical prerequisites, and any specific remaining Origin decisions. No 90-frame execution, no new math, no kernel changes, no code changes before declaration review.
