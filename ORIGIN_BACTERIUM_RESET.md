# ORIGIN RESET — Artificial Bacterium, Complete Relational Architecture

**Date:** 2026-11-07  
**Status:** GOVERNING BUILD RESET; not evidence that implementation has been completed  
**Scope:** Replace the iterative A-first bacterium design with a declaration-first organism.  
**Mathematical authority:** unchanged canonical `abr-kernel` V9.  
**Execution:** `abr-relational-processor`, after inspection of actual source/API.  
**Do not use IRRS or add a validation framework.**

## 1. Stop patching the previous experiment

The previous run3 implementation is **not** the design authority. Its webcam readings and reports may inform the new experiment, but do not inherit its node/edge choices, initialization, or evaluation order without examining the canonical kernel. No need to retain superseded control runs for their own sake. The **current** experiment must retain enough raw data and provenance to reproduce its claims.

**Do not start by editing `closed_loop.rs`.** First inspect and document the canonical kernel's actual operator definitions, inputs, topology requirements, primary-region behavior, temporal requirements, and the processor's field/declaration API. Record exact commits. Do not assume R is a temporal derivative, or that its eligibility is determined by the availability of an earlier camera frame: establish the actual rule from source.

## 2. Organism as one field

The organism is the bounded relational field. Its inherited **genetic declaration** establishes:
- receptor, actual measurement mapping M, units (green-channel DN), frame provenance and validity;
- memory structure, first-measurement implantation, retention and retrieval rules;
- complete A/B/R/ρ/continuation/persistence **evaluation structure** through the canonical kernel;
- observable field loci and physically or operationally justified directed relations, with their meaning and provenance;
- body state and the distinction between software sampling-coordinate commands and independently observed physical motion;
- a separately declared motor policy, P-1 if retained by Origin, which consumes a specified canonical output but does not determine which operators run;
- episodic records for observations, memory, kernel outputs, commands and subsequent measured consequences.

Genes configure the organism, not canonical mathematics. Genetic inheritance is not a fabricated historical observation. Learning/adaptive policy changes are **not** established merely by memory and P-1.

## 3. First measurement before the simulation loop

1. Acquire a **real** camera measurement at the declared receptor coordinate before the behavioral simulation loop.
2. Record its provenance and immediately write the measured value to memory.
3. If the organism's declared topology requires a retrieval locus, read the implanted value back through an actual recorded memory operation; do not equate retrieval with a fictitious earlier observation.
4. Construct the first field from **actually present** values and declared relationships.
5. Evaluate **all** canonical operators whose requirements are satisfied by this field. Do not impose a blanket 'first frame means no R' rule. Where an operator cannot run, identify the exact canonical missing prerequisite.
6. Start the behavior loop only after this initial field and memory have been established. Each later reading compares against actual retained memory, with the correct read/write order.

No synthetic k=-1, zero R by convention, invented persistence state, or made-up topology. The recording begins during an already evolving process; this does not make unobserved prior numerical values available.

## 4. All operators from the original structure

**A, B, R and all applicable canonical derived/persistence operations must be wired into the original mathematical structure.** Do not build an A-only organism and append R later.

At **every** observation, evaluate the full set of eligible canonical operations over the admitted field. A primary region or any other unsupported operator location must be documented using **actual kernel definitions**, not application convenience. In particular, distinguish:
- lack of sufficient **spatial/relational structure** for R;
- lack of a **prior temporal state** for persistence;
- missing or invalid observed measurements;
- policy consuming only A while the full field still evaluates B/R.

These are different conditions. The processor must expose which operator ran, what it received and what it returned; no silent omissions.

## 5. Provenance and observable correspondence

For every sampled state, save the original camera measurement, acquisition/frame identifier and timestamp semantics, memory source, complete submitted field/declaration, actual canonical operator inputs/outputs, policy input/command, next sampled coordinate, and next camera reading.

Compare:
- observed values against memory and submitted operator inputs;
- A/B/R and persistence against their **canonical definitions and available observed relations**, without reimplementing mathematics as a second authority;
- declared command mapping against emitted command;
- command target against actual recorded next sampling coordinate;
- subsequent observed sensor reading against any **explicitly made** prediction, if one exists.

Do not call commanded software movement independent physical movement. Do not claim R causes a motor response when policy uses A. Do not call numerical agreement with the same input data independent physical predictive validation. Report calculated/observed/OPEN separately.

## 6. Strict build order and stop conditions

**Phase 0 — canonical source audit.** Read the actual `abr-kernel` and `abr-relational-processor` source. Produce a short table of operator prerequisites, especially R primary-region and persistence, with source paths and lines. **Stop** if source cannot be inspected.

**Phase 1 — genetic and field declaration.** Define D, M, topology, units, provenance, initial memory and all canonical operator calls together. Explicitly justify the receptor/store/retrieval edges or revise them if they are merely software-event order. Present the complete declaration for Origin review **before writing experiment code**.

**Phase 2 — minimal executable.** Implement one initial real measurement and a single successor measurement. Show every eligible canonical output, including R, and all non-eligibility reasons. No motor loop yet.

**Phase 3 — bounded closed loop.** Only after Phase 2 review, run the 90-step camera/sampling-coordinate experiment, with complete operator evaluation and declared motor policy. Produce per-step observation-to-operator-to-observed-outcome evidence.

**Phase 4 — observational review.** Report actual correspondence, discrepancies, OPEN cases and source versions. Tests are useful for software conformance, but verification of behavior requires observation.

**Stop on:** missing kernel/processor source, unauthorized mathematical choices, invented R prerequisites, missing provenance, fabricated prior, ungrounded directed edges, or inability to distinguish observed measurements from commanded state.

## 7. Required first response from Claude

Before any code edits, return:
1. Exact kernel and processor commits and cited source locations for A/B/R and persistence prerequisites.
2. Proposed complete genetic declaration, field D/M, loci, edges, and direction/provenance.
3. What R can calculate at implanted k0, what it cannot, and **why according to kernel source**.
4. The two-observation execution plan and what will be measured.
5. Every unresolved mathematical or observational decision requiring Origin approval.

**Do not run the 90-frame experiment, alter canonical mathematics, or commit implementation until this review is complete.**
