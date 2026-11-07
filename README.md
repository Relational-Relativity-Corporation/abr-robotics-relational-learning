# ABR Robotics Relational Learning

An NVIDIA Isaac Sim research demonstration of an **embodied robot as one continuously evolving relational field**, integrating sensory observations, motor consequences, episodic experience, and future learning through Metatron Dynamics' canonical ABR mathematics.

> **Start here:** [DECLARATION.md](DECLARATION.md) — governing architecture, mathematical constraints, status ledger, and next-session handoff.

## Project objective

Build outward from a small, executable, observationally verified mathematical core. The robot **is the field**. Sensors, actuators, body configuration, environmental observations, and retained experiences are aspects of one relational process; A, B, and R are evaluated over the admitted field through the existing canonical kernel, not separately reinvented for each subsystem.

The intended demonstration uses a mobile robot, 360° LiDAR, independently moving probes, and eventually a bounded episodic learning mechanism. The research questions are whether it can adapt based on observed consequences, and how much **total computation** is required for the **same measured behavior** versus a conventional baseline.

## Dependencies and reuse

- **Mathematical authority:** `abr-kernel` V9 — canonical operators and admission rules.
- **Integration target:** `abr-relational-processor` — inspect actual APIs before writing adapters.
- **Reusable work:** `abr-dynamixel`, `abr-robotics-demo`, and related existing repositories, after compatibility review.
- **Simulation target:** NVIDIA Isaac Sim. No simulator integration is asserted as complete.

Do not duplicate A/B/R, introduce new mathematical authority, or infer graph edges from LiDAR scan order.

## Development order

1. Inspect canonical kernel and processor; pin commits and inventory supported declarations.
2. Declare a minimal bounded field: robot observations plus one observed probe, with physical topology and compatible measurement mappings.
3. Run canonical evaluation over successive recorded observations and compare results with actual observations.
4. Establish a verified sensorimotor loop.
5. Expand to multiple moving probes and declared behavioral objectives.
6. Add episodic retention and a separately declared learning policy, without modifying canonical mathematics.
7. Benchmark end-to-end compute and behavior against a fair conventional controller.

## Evidence and honesty

**Current status:** architecture declared; new-repository implementation, live learning, physical correspondence, and computational advantage **not yet verified**. Tests and calculations are not substitutes for observation. The declaration file records OPEN questions and the exact next-session starting procedure.

## Morning handoff — 2026-11-07

Read `DECLARATION.md` first. **Do not start by building an Isaac Sim scene or inventing learning mathematics.** Start with the existing `abr-relational-processor` and `abr-kernel` source, establish a declaration inventory and one bounded observed relational field, execute the operators where admissible, and compare their outputs with recorded observations. Preserve the status ledger and stop on unauthorized mathematical choices.
