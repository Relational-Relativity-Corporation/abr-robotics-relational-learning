# BUILD HANDOFF — Genetic Organization, First Memory, and Observable Operator Correspondence

**Date:** 2026-11-07  
**Status:** Origin-directed build clarification; implementation and observational correspondence pending review  
**Scope:** Existing webcam artificial-bacterium experiment; preserve original evidence  
**Mathematical authority:** canonical `abr-kernel` V9 alone  
**Execution integration:** existing `abr-relational-processor`  
**Retired dependency:** do not reintroduce IRRS or create a new black-box validation gate.

## 1. Governing declaration

**The organism's genetic organization establishes its inherited sensor, memory, relational-processing, motor, and body mechanisms. The first measurement is the first memory.**

The first recorded measurement is a legitimate observation and is retained immediately. The first observation is **not** a fabricated prior, and lack of an earlier recorded measurement must not cause that first observation to be discarded. A continuous physical process predates the recording window; recording begins at an arbitrary observation boundary.

Distinguish four events precisely:
1. First legitimate recorded observation (k=0).
2. First memory write retaining that observation.
3. First operator evaluation for which all canonical inputs and preconditions actually exist.
4. First admissible temporal continuation or persistence evaluation.

No claim is made that every operator must produce an output at k=0. Never invent observation k=-1, an initial R, or an initial persistence value to force execution.

## 2. Inherited genetic organization versus acquired experience

The bacterium's **genetic declaration** defines the organism-specific, pre-existing organization:
- **Receptor:** the source, location, channel, measurement mapping, units, range and acquisition provenance of its sensory readings.
- **Memory apparatus:** first-observation retention; read-before-write on subsequent observations; provenance-preserving retrieval and update.
- **Relational apparatus:** invocation of the unchanged canonical kernel on admitted observed relationships, with each operator's actual prerequisites respected.
- **Motor interface and policy:** explicitly declared P-1 mapping from a specified canonical output to direction, including step size, boundaries, and no-output behavior. This is organism-specific behavior policy, not kernel mathematics.
- **Body and environment interface:** the recorded receptor sampling coordinate and the camera acquisition it selects. A commanded coordinate is not independently observed physical displacement.
- **Episodic record:** retain measured inputs, kernel outputs, chosen commands and subsequent observations, with provenance.

Genes define **capacity and inherited rules**, not the numerical content of an observation or a substitute for the canonical operators. Learned changes to policy are not yet implemented and must not be claimed.

The genetic declaration is separate from, and subordinate to, the canonical kernel's mathematical definitions. Do not create a second operator implementation or admission framework.

## 3. Mandatory observed process

At k=0: acquire actual camera reading; record its frame identity, pixel coordinate, green-channel DN and acquisition timing; retain it immediately as memory 0; record that no earlier observation exists. The first observation is valid even if a particular operator cannot yet run.

At k>=1: acquire a new actual reading; retrieve the genuinely retained prior observation before updating memory; construct only provenance-supported relational inputs; execute eligible canonical operators through `abr-relational-processor`; apply the separately declared P-1 command mapping where its required canonical output exists; record the command and the next acquisition coordinate and reading; retain the current observation.

Never treat event order alone as sufficient proof of a physically meaningful coupling. Audit the exact provenance of the receptor→store and store→retrieval edges and the interpretation of their direction and units.

## 4. R and persistence: inspect, do not patch

Inspect the canonical kernel source and the processor's invocation of R, rho, and persistence. Determine exactly what each requires at the first observation and first continuation. Separate:
- a valid first measurement;
- a stored first measurement;
- an admitted spatial relation at that measurement;
- availability of prior relational state for temporal operators.

If the processor incorrectly rejects k=0 merely because no prior measurement exists, correct **application-level observation handling** without changing kernel mathematics. If a canonical operator legitimately requires unavailable prior data, record that operator as not evaluated at that step. Never initialize R by convention, force a zero, or invent a past state.

Use only explicitly Origin-declared parameters for this organism; preserve provenance for rho_base=0.5 and chi_0=1 DN as reported in the current experiment, and verify they are actually carried in the declaration submitted to the processor.

## 5. Observable provenance and mathematical rigor

For every observation and operator evaluation, record:
- measured camera data and original frame identifier/hash;
- exact memory value and the earlier observation from which it came;
- field nodes, edges, direction, mapping and units, with provenance;
- exact kernel inputs, functions invoked and outputs;
- P-1 input, selected command, resulting sampling coordinate and next actual reading;
- direct comparison between kernel results and the measured values they describe;
- any difference, unresolved precondition or claim unsupported by observation.

**Verification = observation.** Do not add a black-box verifier, independent mathematical authority, arbitrary score, or invented acceptance threshold. Passing Rust tests confirms software behavior, not physical correspondence. R and persistence execution alone do not prove that those outputs predict physical behavior.

## 6. Bounded build and evidence procedure

1. Inspect current local files and preserve `evidence/run2_memory/` and `evidence/run2_no_memory/` unchanged, including hashes. These are the reported original 90-frame webcam runs; do not silently overwrite them.
2. Identify the exact code path that currently rejects k=0 and conflates observation validity with eligibility of a prior-dependent operator.
3. Add an explicit, human-readable **genetic declaration** for the bacterium; use existing code/declarations rather than duplicating definitions. Mark what is inherited, measured, calculated, commanded and still OPEN.
4. Make the smallest code change necessary to retain k=0 as the first memory and preserve all observed states. Keep operator eligibility canonical.
5. Run existing tests plus focused first-observation, second-observation, R/persistence-prerequisite, provenance and command-response tests.
6. Execute a new, separately identified bounded camera run. Preserve raw acquisition, exact declarations, kernel outputs and behavioral records. Compare with the original run only where experimental conditions support comparison.
7. Report observed agreement, disagreement and unresolved correspondence. Do not call a stationary sampled coordinate a moving physical bacterium, or claim learning from P-1 alone.
8. Return changed files, exact kernel/processor commits, reproducible commands, and evidence paths. **Do not merge or claim observational verification before Origin review.**

## 7. Expected report

Answer explicitly:
- Was k=0 recorded and retained as memory 0?
- What was the first legitimately evaluable canonical A, B, R and persistence output, respectively, and why?
- Were any edges admitted solely because software events were sequential?
- For each motor command, what was commanded, what coordinate was actually used for the next acquisition, and what camera reading followed?
- Which operator outputs correspond to independently observed quantities, and which are only calculated states?
- Did any original evidence change? Did the canonical kernel change? (Both must remain unchanged.)

**Stop on any unauthorized mathematical choice. Build and measure rather than inventing another validation system.**
