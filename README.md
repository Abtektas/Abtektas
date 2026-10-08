<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img alt="Ahmet Burak Tektas: robotics, autonomous-driving simulation and local LLMs" src="assets/header-light.svg" width="100%">
</picture>

I'm Burak, based in Oslo. Mostly I contribute upstream to open-source robotics, autonomous-driving simulation and local LLM projects.

<a href="https://linkedin.com/in/abtektas"><img alt="Connect on LinkedIn" src="https://img.shields.io/badge/Connect_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"></a>

### Open-source contributions

<!-- CONTRIBUTIONS:START -->
**28** pull requests to **8** projects · ✅ 19 merged · 👍 1 approved · ⏳ 8 in review

#### [PX4 Autopilot](https://github.com/PX4/PX4-Autopilot)
Drone flight stack: fixed-wing Offboard and rover fixes.

- ⏳ [fix(fw_mode_manager): clear the course setpoint in Offboard \[1.18\]](https://github.com/PX4/PX4-Autopilot/pull/29025) <sub>in review, opened Oct 7, 2026</sub>
- ⏳ [fix(ekf2): stop the test replay at the end of the sensor data](https://github.com/PX4/PX4-Autopilot/pull/28958) <sub>in review, opened Oct 1, 2026</sub>
- ⏳ [fix(control_allocation): scale thrust by the actuators producing it](https://github.com/PX4/PX4-Autopilot/pull/28953) <sub>in review, opened Oct 1, 2026</sub>
- ✅ [fix(fw_mode_manager): clear the course setpoint in Offboard](https://github.com/PX4/PX4-Autopilot/pull/28920) <sub>merged Sep 30, 2026</sub>
- ✅ [fix(rover): silence missing HIWONDER_EMM_EN on builds without the driver](https://github.com/PX4/PX4-Autopilot/pull/28887) <sub>merged Oct 5, 2026</sub>

#### [Magistrala](https://github.com/absmach/magistrala)
IoT platform: message reader time bounds, CLI docs and certificate Makefile fixes.

- ✅ [MG-3628 - Write the certificate configs without the GNU Make 4 file function](https://github.com/absmach/magistrala/pull/3629) <sub>merged Oct 7, 2026</sub>
- ✅ [MG-3148 - Document the users commands in the CLI README](https://github.com/absmach/magistrala/pull/3627) <sub>merged Oct 7, 2026</sub>
- ✅ [MG-3621 - Use the created column for time bounds of JSON formats](https://github.com/absmach/magistrala/pull/3623) <sub>merged Oct 1, 2026</sub>

#### [ArduPilot](https://github.com/ArduPilot/ardupilot)
Drone flight stack: SITL autotests and HAL test fixes.

- ⏳ [Plane: set tailsitter enable before creating the VTOL AHRS view](https://github.com/ArduPilot/ardupilot/pull/34643) <sub>in review, opened Oct 6, 2026</sub>
- 👍 [autotest: fix and re-enable Plane.TerrainRally](https://github.com/ArduPilot/ardupilot/pull/34517) <sub>approved, opened Sep 27, 2026</sub>
- ✅ [AP_HAL: fix DSP_test reading past the end of gyro_frames](https://github.com/ArduPilot/ardupilot/pull/34502) <sub>merged Oct 6, 2026</sub>

#### [MAVProxy](https://github.com/ArduPilot/MAVProxy)
MAVLink proxy and command-line ground station: console completion fixes.

- ✅ [OpenDroneID: use the UTC epoch for the 2019 timestamp](https://github.com/ArduPilot/MAVProxy/pull/1767) <sub>merged Oct 8, 2026</sub>
- ✅ [rline: don't let a short completion rule break the others](https://github.com/ArduPilot/MAVProxy/pull/1765) <sub>merged Oct 1, 2026</sub>

#### [CARLA](https://github.com/carla-simulator/carla)
Autonomous-driving simulator: Python API agents, examples and docs.

- ✅ [docs: fix broken internal links](https://github.com/carla-simulator/carla/pull/9927) <sub>merged Oct 5, 2026</sub>
- ✅ [fix(python): report spawn failures in the collision determinism smoke test](https://github.com/carla-simulator/carla/pull/9923) <sub>merged Oct 2, 2026</sub>
- ✅ [docs: fix code examples in the guides that fail when run](https://github.com/carla-simulator/carla/pull/9922) <sub>merged Oct 2, 2026</sub>
- ✅ [docs(python): fix the Python API snippets and remaining keyword names](https://github.com/carla-simulator/carla/pull/9921) <sub>merged Oct 1, 2026</sub>
- ✅ [fix(python): import sys in the manual_control examples](https://github.com/carla-simulator/carla/pull/9920) <sub>merged Oct 1, 2026</sub>
- ✅ [docs(python): use the bindings' keyword argument names](https://github.com/carla-simulator/carla/pull/9918) <sub>merged Sep 30, 2026</sub>
- ✅ [docs: state that actor velocities use world coordinates](https://github.com/carla-simulator/carla/pull/9916) <sub>merged Sep 30, 2026</sub>
- ✅ [docs: update walker skeleton tutorial to the current bone API](https://github.com/carla-simulator/carla/pull/9915) <sub>merged Sep 30, 2026</sub>
- ✅ [fix(agents): handle a missing incoming waypoint in BehaviorAgent](https://github.com/carla-simulator/carla/pull/9912) <sub>merged Sep 29, 2026</sub>
- ✅ [fix(python): honour --show-* flags in no_rendering_mode map cache](https://github.com/carla-simulator/carla/pull/9910) <sub>merged Sep 29, 2026</sub>

#### [pymavlink](https://github.com/ArduPilot/pymavlink)
MAVLink Python library and code generators: Swift generator fix.

- ⏳ [generator: Swift: use the XML bitmask attribute for option sets](https://github.com/ArduPilot/pymavlink/pull/1299) <sub>in review, opened Oct 1, 2026</sub>

#### [QGroundControl](https://github.com/mavlink/qgroundcontrol)
Ground control station: MAVLink COMMAND_INT support and mission command handling.

- ⏳ [fix(PX4): send DO_REPOSITION as COMMAND_INT when supported](https://github.com/mavlink/qgroundcontrol/pull/15187) <sub>in review, opened Sep 25, 2026</sub>
- ⏳ [fix(Vehicle): send DO_SET_HOME as COMMAND_INT when supported](https://github.com/mavlink/qgroundcontrol/pull/15186) <sub>in review, opened Sep 25, 2026</sub>
- ✅ [fix(MissionManager): restore mission commands lost to broken enum translations](https://github.com/mavlink/qgroundcontrol/pull/15185) <sub>merged Sep 29, 2026</sub>

#### [Ollama](https://github.com/ollama/ollama)
Local LLM runtime: MLX runner and Gemma 4 mixture-of-experts loading on Apple Silicon.

- ⏳ [mlxrunner: load gemma4 experts in the mlx-lm switch_glu layout](https://github.com/ollama/ollama/pull/18631) <sub>in review, opened Sep 24, 2026</sub>
<!-- CONTRIBUTIONS:END -->

<sub>Last updated Oct 8, 2026 by [GitHub Actions](.github/workflows/update-readme.yml)</sub>
