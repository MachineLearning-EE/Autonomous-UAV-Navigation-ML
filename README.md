# 🚁 Autonomous UAV Navigation — ML Based Obstacle Avoidance

> ROS2 + PX4 + Gazebo SITL · LiDAR Obstacle Avoidance · LLaMA Decision Making (Phase 2)

---

## 📌 Project Overview

This project builds a fully autonomous UAV navigation system in two phases:

- **Phase 1** — Rule-based reactive navigation (if/else logic) with ROS2 + PX4 + Gazebo simulation ✅
- **Phase 2** — LLM-based intelligent decision making using LLaMA + model validation 🔜

The drone automatically arms, takes off, detects obstacles using LiDAR, avoids them, and navigates to a goal — all without human intervention.

---

## 🗂️ Repository Structure

```
Autonomous-UAV-Navigation-ML/
│
├── src/                              # ROS2 source package
│   └── llm_drone/
│       ├── llm_drone/
│       │   ├── __init__.py
│       │   └── autonomous_flight_lidar.py   # Phase 1: Rule-based control node
│       ├── package.xml
│       ├── setup.py
│       └── setup.cfg
│
├── PX4-gazebo-models-main/           # Gazebo drone & world models
│   ├── models/                       # Drone SDF models (x500, lidar, etc.)
│   ├── worlds/                       # Simulation environments
│   └── tools/                        # Model validation scripts
│
├── README.md
└── Machine_Learning_Based_Autonomous_UAV_Control.pdf   #REFERENCE PAPER
```

---

## 🔵 Phase 1 — Rule-Based Navigation (Current / Midsem) ✅

### What it does
- ✅ Auto arm and takeoff to safe altitude (3m)
- ✅ LiDAR-based obstacle detection (360° scan)
- ✅ Rule-based avoidance — steers left or right based on clearance
- ✅ Goal-directed navigation using position vector
- ✅ Full ROS2 ↔ PX4 offboard control integration

### Decision Logic (if/else)
```
IF front_distance < 2.0m:
    IF left_clearance > right_clearance → steer LEFT
    ELSE → steer RIGHT
ELSE:
    move toward GOAL
```

### System Architecture
```
Gazebo Simulation → PX4 Flight Controller ↔ ROS2 DDS Bridge
                                ↕
                    AutonomousFlight Node
                    1. Arm drone
                    2. Switch OFFBOARD mode
                    3. Takeoff control
                    4. LiDAR obstacle detection
                    5. Rule-based path adjustment
                    6. Waypoint navigation
                                ↓
                    TrajectorySetpoint → Drone Movement
```

---

## 🟡 Phase 2 — LLM Decision Making (Upcoming / Endsem) 🔜

### Planned features
- 🔜 Replace if/else logic with **LLaMA** language model decisions
- 🔜 Complex Gazebo world environments for testing
- 🔜 Model validation and performance benchmarking
- 🔜 Comparison: Rule-based vs LLM-based navigation

### Phase 2 Architecture
```
LiDAR Data + Drone State
        ↓
  LLaMA Decision Module
  (replaces if/else logic)
        ↓
  Trajectory Command → PX4 → Drone Movement
```

---

## ⚙️ Prerequisites

- Ubuntu 22.04
- ROS2 Humble
- PX4 Autopilot (SITL)
- Gazebo Garden / Harmonic
- `px4_msgs` ROS2 package
- Python 3.10+, NumPy
- **Phase 2 only:** Ollama + LLaMA 3 model

---

## 🚀 Setup & Run (Phase 1)

### 1. Clone the repository
```bash
git clone https://github.com/MachineLearning-EE/Autonomous-UAV-Navigation-ML.git
cd Autonomous-UAV-Navigation-ML
```

### 2. Copy PX4 Gazebo models
```bash
cp -r PX4-gazebo-models-main/models ~/.gz/models/
cp -r PX4-gazebo-models-main/worlds ~/.gz/worlds/
```

### 3. Build the ROS2 workspace
```bash
colcon build
source install/setup.bash
```

### 4. Launch PX4 SITL with Gazebo
```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

### 5. Run the autonomous flight node
```bash
ros2 run llm_drone autonomous_flight_lidar
```

---

## 📡 ROS2 Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/fmu/in/offboard_control_mode` | `OffboardControlMode` | Publish |
| `/fmu/in/trajectory_setpoint` | `TrajectorySetpoint` | Publish |
| `/fmu/in/vehicle_command` | `VehicleCommand` | Publish |
| `/fmu/out/vehicle_odometry` | `VehicleOdometry` | Subscribe |
| `/scan` | `LaserScan` | Subscribe |

---

## 🚁 Drone Models Included

| Model | Description |
|-------|-------------|
| `x500_lidar_2d` | X500 quadrotor with 2D LiDAR |
| `x500_lidar_front` | X500 with front-facing LiDAR |
| `lidar_2d_v2` | Standalone 2D LiDAR sensor |
| `default.sdf` | Default Gazebo world |
| `walls.sdf` | Obstacle wall environment |
| `forest.sdf` | Forest obstacle environment |

---

## 📊 Phase Comparison

| Feature | Phase 1 ✅ | Phase 2 🔜 |
|---------|-----------|-----------|
| Decision Making | Rule-based if/else | LLaMA LLM |
| Obstacle Avoidance | Reactive (greedy) | Intelligent |
| Simulation | Basic SITL | Complex Gazebo worlds |
| Validation | Visual inspection | Quantitative benchmarks |

---

## 📄 Research Paper

See [`Machine_Learning_Based_Autonomous_UAV_Control.pdf`](./Machine_Learning_Based_Autonomous_UAV_Control.pdf) for the full project report.

## 📚 References

1. Gupta et al., "Cooperative multi-agent control using deep reinforcement learning," 2019.
2. Ross et al., "A reduction of imitation learning to no-regret online learning," AISTATS 2011.
3. Giusti et al., "A machine learning approach to visual perception of forest trails," IEEE RA-L 2016.
4. Shah et al., "AirSim: High-fidelity simulation for autonomous vehicles," 2018.
5. Abbeel et al., "Autonomous helicopter aerobatics through apprenticeship learning," IJRR 2010.

## 📝 License

MIT License
