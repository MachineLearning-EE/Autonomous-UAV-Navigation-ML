# 🚁 Machine Learning Based Autonomous UAV Control

Autonomous drone navigation system using **ROS2 + PX4 + Gazebo** with LiDAR-based obstacle avoidance.

## 📋 Overview

This project implements a ROS2 node (`autonomous_flight_lidar`) that controls a UAV in a simulated environment using PX4 in OFFBOARD mode. The drone can:

- ✅ Auto arm and take off
- ✅ Detect obstacles using LiDAR (`/scan` topic)
- ✅ Avoid collisions by steering left or right
- ✅ Navigate toward a defined goal waypoint

## 🗂️ Project Structure

```
drone_llm_ws/
└── src/
    └── llm_drone/
        ├── llm_drone/
        │   ├── __init__.py
        │   └── autonomous_flight_lidar.py   # Main ROS2 node
        ├── package.xml
        ├── setup.py
        └── setup.cfg
```

## ⚙️ System Architecture

```
Gazebo Simulation  →  PX4 Flight Controller  →  ROS2 Communication Layer
                                ↕
                    Autonomous Control Node
                    1. Arm drone
                    2. Switch OFFBOARD mode
                    3. Takeoff control
                    4. Obstacle detection (LiDAR)
                    5. Path adjustment
                    6. Waypoint navigation
                                ↓
                    Trajectory Setpoints → Drone Movement
```

## 🛠️ Prerequisites

- Ubuntu 22.04
- ROS2 Humble
- PX4 Autopilot (with SITL / Gazebo)
- `px4_msgs` ROS2 package
- Python 3.10+, NumPy

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/drone_llm_ws.git
cd drone_llm_ws
```

### 2. Build the workspace
```bash
colcon build
source install/setup.bash
```

### 3. Launch PX4 SITL with Gazebo
```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

### 4. Run the autonomous flight node
```bash
ros2 run llm_drone autonomous_flight_lidar
```

## 🤖 How It Works

The `AutonomousFlight` node runs a control loop at 10 Hz:

| Phase | Counter | Action |
|-------|---------|--------|
| Takeoff | 0–50 | Climb to -3.0 m (NED frame) |
| OFFBOARD | 60 | Switch flight mode |
| Arm | 70 | Arm the drone |
| Navigate | 70+ | Goal-directed + obstacle avoidance |

### Obstacle Avoidance Logic

LiDAR scan is divided into three zones:
- **Front** – first and last 20 readings
- **Left** – readings 60–120
- **Right** – readings 340–300 (mirrored)

If the front zone detects an obstacle within **2.0 m**, the drone steers toward whichever side has more clearance.

## 📡 ROS2 Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/fmu/in/offboard_control_mode` | `OffboardControlMode` | Publish |
| `/fmu/in/trajectory_setpoint` | `TrajectorySetpoint` | Publish |
| `/fmu/in/vehicle_command` | `VehicleCommand` | Publish |
| `/fmu/out/vehicle_odometry` | `VehicleOdometry` | Subscribe |
| `/scan` | `LaserScan` | Subscribe |

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
