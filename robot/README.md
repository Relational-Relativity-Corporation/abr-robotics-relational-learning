# Four-component canonical observation execution

The active entry point is `robot/run_experiment.py`. It acquires actual simulated
component I/O and invokes canonical Kernel V9 A, rho, B, R and persistence. It
contains no operator-to-actuator mapping and issues no actuator commands.
Stationary observations are a valid execution result, not a failure to approach.

Stage 1, field identity, N1..N4, E1..E12, geometry, numerical M, and Kernel parameter
selection are unchanged. `config.json` explicitly records an absent mapping as
`operator_to_actuator_mapping: null`. A non-null entry is refused rather than
treated as permission to synthesize a controller.

## Run and test

From the repository root:

```
cargo test --manifest-path robot/kernel_bridge/Cargo.toml --locked
cargo build --manifest-path robot/kernel_bridge/Cargo.toml --locked
cd robot
python -B -m unittest discover -v
python -B run_experiment.py --output ../evidence/NEW-UNUSED-DIRECTORY
python -B verify_evidence.py ../evidence/NEW-UNUSED-DIRECTORY --replay-kernel
```

The finite observation protocol acquires five samples at each of the existing
two object placements. Relocation is an experimenter operation, never a robot
decision. One live bridge retains actual prior outputs across all ten states.
The fixed sample count is an acquisition protocol, not a stopping algorithm.
No target tolerance, clearance error or target-attainment test controls runtime.

## Removed behavior

The former `drive_projection` was deleted, not replaced:

- Clearance minus target error and tolerance-based stopping.
- Absolute R[E2] selection and proportional drive gain.
- Behavioral speed cap and minimum-based approach speed selection.
- Quarter-error motion budget and error/pulse-duration speed calculation.
- Conversion of that generated speed into wheel commands.
- Five-target-observation termination and approach-success scoring in the runner.

No explicit zero-speed actuator command is substituted. `RobotObserver` returns
`command: null` and records that no Origin-authorized operator-to-actuator mapping
exists. The runner does not call `PythonRobot.apply`. Physics initializes and
evolves an idle motor; motor feedback is still sampled, not fabricated.

## Preserved D/M and physical calculations

| Node | Supplied value | Role |
|---|---|---|
| N1 Robot Body | LiDAR-to-front offset | Declared geometry readback, m |
| N2 LiDAR Sensor | Valid forward range | Simulated proximity observation, m |
| N3 Motor Actuator | Wheel radius times mean actual shaft encoder angle | Simulated feedback projection, m |
| N4 Genetic Memory | Persistent 0.1 m instruction readback | Declared objective, m; not a behavioral rule |

The chassis remains 240x180 mm, wheel radius 30 mm, track 112.5 mm, front face
x=0.12 m and LiDAR mount (0,0,0.16) m. Forward clearance is observed range minus
the 0.12 m mounting offset. The target therefore corresponds to 0.22 m sensor
range, within the unchanged A1 limits 0.15..12 m.

Preserved ordinary physical arithmetic includes sensor ray/circle intersections,
bearing and acquisition-time calculations, validity checks, shaft encoder unit
conversion, finite motor acceleration and saturation, differential-drive
kinematics, numerical physics integration, and independent evaluation geometry.
These operations generate/convert component information or model physics. They
do not select behavioral objectives or turn Kernel outputs into decisions.
The motor `apply` interface remains for hardware/physics tests, outside the
active observation runner. The Isaac adapter likewise retains only physical
signal conversion and actuator I/O, with no relational decision projection.

M deliberately retains distinct roles despite a common metre-valued component:
geometry, range, encoder travel and reference. All twelve directed software inbox
deliveries retain their identities and recorded source payloads. No fake feedback
or duplicate range is introduced to populate another node.

## Canonical authority and evidence

All operator values come from the unchanged sibling `abr-kernel` through
`diagnostic_exec::execute_spatial` and `execute_with_prior`. Kernel revision is
recorded per execution; no operator formulas are implemented here. The first
observation has no fabricated prior. Persistence continues across relocation.

Every fresh output directory contains raw LiDAR scans, component packets,
twelve deliveries per state, exact node inputs, canonical numerical outputs
and f64 bits, raw diagnostics, actual idle actuator state, separate world-state
evaluation, source/config snapshots and a SHA-256 manifest. Existing evidence is
never overwritten. Exit success describes operator execution, not objective
attainment or motion.

The original `robot/evidence/stage3-first-closed-loop.zip`, its verification JSON,
and original repository evidence remain immutable historical records. Their
approach results depended on the now-removed controller and do not establish
operator-only behavioral success. Historical target checks in the read-only
evidence verifier audit those saved results only; they are not executable robot
decision logic. Canonical replay uses each artifact's saved configuration.

The older untracked `organism/` phototaxis work is not imported or executed by
this four-node runner. It is unrelated legacy work, not an alternate actuator
mapping for this field.

## Isaac Sim

The active Python environment lacks Isaac Sim. Its existing component adapters
and configured Jetbot asset reference are retained, with SDK/model execution
still unverified. No new simulator integration, learning or behavioral mapping
is introduced in this change.
