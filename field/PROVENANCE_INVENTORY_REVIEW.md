# Provenance inventory — four-node / twelve-edge field

Status: **REVIEW DRAFT — NOT AN EXECUTABLE D/M ADMISSION**. This document records observed software provenance and separates it from candidate relational meanings. It does not assign new mathematical values, change topology, or authorize actuation. Origin must confirm the observable meaning of each edge before it is used as a numerical relationship.

## Governing rule

Every node and edge must identify observable identity, source, destination, quantity, unit, reference frame, acquisition time, validity, and provenance before its value enters executable M. A routed packet is not itself an independently measured edge quantity. Canonical A, B, R, rho operate on the whole admitted field; no parallel behavioral mathematics is authorized. Missing observations are not zero-padded, averaged, or fabricated.

## Nodes — current published implementation

| ID | Identity | Actual published source | Numerical M | Information not included | Status |
|---|---|---|---|---|---|
| N1 | Robot body | robot/config.json geometry; robot/signals.py geometry_packet | lidar_to_front_m = 0.12 m (configuration readback) | measured pose, body movement, additional geometry | Partial |
| N2 | LiDAR | robot/substrate.py scan() simulated beams; robot/signals.py forward_return() | one valid forward range in m | bearing, other returns, timestamps, validity | Partial |
| N3 | Two-wheel motor actuator | robot/substrate.py motor_packet() simulated left/right encoder and velocity | wheel_radius × mean encoder angle in m | independent left/right command, position, velocity, torque | Collapsed |
| N4 | Genetic memory | robot/signals.py InstructionMemory persisted JSON | front_clearance_target_m only | SEEK disposition and inherited response semantics | Partial |

Origin's current clearance objective is 0.15 m from robot front. The published main config inspected for this inventory still says 0.10 m; local uncommitted changes reportedly set 0.15 m. Do not treat the older config as current authorization.

## Edges — source packet vs candidate meaning

All edges are declared in field/stage1_robotics_domain.json as generic directed information relationships; their class and numerical edge measurements are null. robot/signals.py InformationRouter.route() copies the **entire source packet** to the destination inbox for each edge, with edge ID, source, target, receiver and generic meaning. None of the candidate meanings below is a verified per-edge measured quantity.

| Edge | From → To | Actual payload delivered | Candidate observable relationship for Origin review | Individually measured numerical edge quantity? |
|---|---|---|---|---|
| E1 | N1 → N2 | N1 source packet | body geometry and mounting relevant to LiDAR observation | **No** |
| E2 | N2 → N1 | N2 source packet | LiDAR range/bearing observation relevant to body | **No** |
| E3 | N1 → N3 | N1 source packet | body wheel geometry relevant to motor action | **No** |
| E4 | N3 → N1 | N3 source packet | independent wheel feedback relevant to body motion | **No** |
| E5 | N1 → N4 | N1 source packet | body state relevant to inherited response | **No** |
| E6 | N4 → N1 | N4 source packet | inherited response relevant to body behavior | **No** |
| E7 | N2 → N3 | N2 source packet | LiDAR stimulus relevant to actuation | **No** |
| E8 | N3 → N2 | N3 source packet | motor action/feedback relevant to subsequent sensing | **No** |
| E9 | N2 → N4 | N2 source packet | LiDAR stimulus relevant to genetic disposition | **No** |
| E10 | N4 → N2 | N4 source packet | inherited disposition relevant to sensing | **No** |
| E11 | N3 → N4 | N3 source packet | motor response feedback relevant to inherited disposition | **No** |
| E12 | N4 → N3 | N4 source packet | inherited disposition relevant to binary motor response | **No** |

## Provenance requirements for each edge

For each E1–E12, Origin must approve a record with: (1) observable relational quantity and operational definition, (2) source measurement(s) and acquisition method, (3) units and reference frame, (4) acquisition time or progression index and synchronization, (5) validity and missing-data rule, (6) numerical projection into M if supported by the canonical Kernel, and (7) evidence linking the value to the physical or persisted source. The edge ID and source packet alone do not satisfy these requirements.

## Known execution limitation

robot/signals.py node_values() reconstructs four scalar values from routed packets; it does not submit independently measured E1–E12 edge quantities. robot/run_experiment.py skips canonical execution when there is no valid forward beam. The current published operator-to-actuator mapping is null. Thus canonical execution is real, but it does not establish genetically driven motor control or complete component provenance.

## Next authorization boundary

Origin should review and approve or correct each candidate edge meaning. Only after this can the generator implement a declaration-driven M that preserves independent left/right motor feedback, LiDAR range and bearing, and an explicitly grounded genetic response. Do not change field topology, invent numerical genetic codes, or introduce control algorithms in this step.

## Inspected source files

- field/stage1_robotics_domain.json
- robot/config.json
- robot/signals.py
- robot/run_experiment.py
- robot/substrate.py
