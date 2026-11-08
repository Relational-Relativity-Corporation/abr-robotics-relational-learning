# Four-component relational robot: first closed-loop experiment

Stage 1 is unchanged. `config.json` declares the engineering geometry, scalar M,
general Kernel parameter selection, and conventional command projection C for
this experiment. It preserves N1..N4 and E1..E12. The twelve software inbox
deliveries are individually logged; they are information relationships, not
invented physical sensor readings. No learning is implemented.

## Run and test

From the repository root (requires Python 3 and Rust; no Python dependencies):

```
cargo test --manifest-path robot/kernel_bridge/Cargo.toml --locked
cargo build --manifest-path robot/kernel_bridge/Cargo.toml --locked
cd robot
python -B -m unittest discover -v
python -B run_experiment.py --output ../evidence/NEW-UNUSED-DIRECTORY
python -B verify_evidence.py evidence/stage3-first-closed-loop.zip --replay-kernel
```

The bridge uses the unchanged sibling `abr-kernel` checkout, recorded as
`833ffb35858f190701583dd59d07e3b67cb2241e` in the first evidence. Check that
revision before reproduction; Cargo.lock pins library dependencies, not the
contents of a path dependency. All operator outputs come directly from
`diagnostic_exec::execute_spatial` / `execute_with_prior`. The older relational
processor's directed-cycle restriction is not used. A single live bridge retains
the actual prior across both trials; observation indices never wrap.

## Geometry and measurement declaration

Python substrate: 240 mm long by 180 mm wide differential-drive chassis, wheel
radius 30 mm, track 112.5 mm. Front face x=0.12 m; LiDAR mount x=0, y=0,
z=0.16 m. Forward beam is aligned with chassis +x. Thus front clearance is
observed forward range minus 0.12 m. The 0.10 m target corresponds to 0.22 m
sensor range, above the unchanged A1 minimum of 0.15 m. The object is a single
100 mm radius cylinder ahead on the floor; only its ray returns reach the robot.

The sensor ray/circle implementation reuses the first-surface calculation from
`abr-robotics-demo/abr_v06_loop.py::lidar_range`; acquisition uses its 8000 Hz,
5.5 rotations/s and 0.15..12 m limits. Each stationary full sweep is indexed from
the forward bearing. No noise or manufacturer accuracy emulation is claimed.
The robot uses stop-and-sense acquisition, finite-acceleration motor pulses,
then braking. There is no continuously moving rolling-scan claim.

M supplies one metre-valued scalar at each component locus:

| Node | Value | Role |
|---|---|---|
| N1 Robot Body | LiDAR-to-front offset read from geometry config | Declared design parameter, not measured body pose |
| N2 LiDAR Sensor | Valid forward beam range | Simulated proximity observation |
| N3 Motor Actuator | Wheel radius times mean actual shaft encoder angle | Simulated encoder feedback, not command or world localization |
| N4 Genetic Memory | 0.1 m read back from persistent instruction JSON | Origin objective, not environmental measurement |

These quantities share a unit but have distinct meanings. Canonical differences
describe this explicitly declared information projection; they are not asserted
to measure physical distances between the four components. All software-routed
cross-component edges are classified Coupling, with information-delivery bases;
physical coupling strengths and physical hardware performance are not asserted.
No value is padded from another node. General rho selection uses the existing
Kernel values with chi unit m; component pairs are empty.

C reads abs(R[E2]) for motion magnitude. Its direction and stop condition read
measured clearance and the fixed instruction. Gain 1/s, 0.15 m/s speed cap,
50 ms pulse, 150 ms braking, and quarter-error pulse budget are explicit
engineering choices. They are not canonical operators. Zero R produces no
motion. Other operator outputs and persistence are calculated and retained,
but are not separate controller inputs. Five consecutive stopped observations
at clearance [0.100, 0.101] m establish the experiment's success condition.

## First observed results

| Trial | Initial measured clearance | Final measured clearance | Samples | Final shafts |
|---|---:|---:|---:|---|
| 1 | 0.680000 m | 0.10077431082725805 m | 166 | Both 0 rad/s |
| 2, after object relocation | 0.5007743108272581 m | 0.1008179149914172 m | 118 | Both 0 rad/s |

Both met the 1 mm tolerance and held for five observations. Minimum forward
sensor ranges were 0.2207743 m and 0.2208179 m. There were 284 spatial evaluations
and 283 persistence pairs, with the same field and actual prior retained when
the experimenter moved the object from x=0.9 m to x=1.3 m. The robot was not reset.
Object positions appear only in the independent evaluator, never controller I/O.

The artifact `evidence/stage3-first-closed-loop.zip` preserves original raw scans,
component packets, twelve deliveries per state, node inputs, canonical numerical
outputs and f64 bits, diagnostics, drive/feedback records, independent evaluations,
source snapshots, summary and SHA-256 manifest. Uncompressed original evidence
remains at repository `evidence/stage3-first-closed-loop/`; it was not overwritten.
This is observed success in a noiseless Python engineering simulation, not a
physical hardware result, an Isaac result, a learning result, or a guarantee
under noise, slip or different objects.

## Isaac Sim convergence

`isaacsim` is not installed in the active Python environment. The executable
fallback is therefore the Python component substrate, as authorized. It does
not claim to be a verified Jetbot dynamics model or XM430 firmware simulation.

Reuse NVIDIA's existing Jetbot USD and wheel joint names in config; do not build
a replacement robot. `isaac_adapter.py::IsaacWheelPort` adapts wheel actions and
actual articulation position/velocity feedback without invoking any pose API.
`laser_scan_packet` accepts a ROS LaserScan and preserves range, bearing,
acquisition time and validity, enforcing the declared A1 limits. It does not
export simulator point clouds, object identity, transforms, maps, or localization.
`author_mount_and_bumper` authors the configured LiDAR mount and physical front
bumper on an existing chassis. These are component geometry, not extra field nodes.

Remaining SDK verification: load the version-compatible Jetbot asset, confirm
its collision bounds/units relative to the declared front bumper, attach a
configured rotary LiDAR at the mount, supply fresh forward-bearing LaserScans,
and step physics through the injected timing interface. Scan origins must match
the mount and axis declaration; unsupported/no forward beam fails closed.
Electrical feedback remains null when the articulation does not provide it.
Adapter contract tests use doubles; live Isaac API/model behavior is unverified.

Sources:

- https://docs.isaacsim.omniverse.nvidia.com/5.1.0/robot_simulation/mobile_robot_controllers.html
- https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.robot.wheeled_robots/docs/index.html
- https://www.slamtec.com/en/lidar/a1spec
- `abr-dynamixel-provisional/abr-dynamixel_build_plan.md`: planning only, not an executable driver.
