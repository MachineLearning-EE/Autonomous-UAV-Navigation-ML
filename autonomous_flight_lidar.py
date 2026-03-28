import rclpy
from rclpy.node import Node

from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleCommand
from px4_msgs.msg import VehicleOdometry

from sensor_msgs.msg import LaserScan
import numpy as np


class AutonomousFlight(Node):

    def __init__(self):
        super().__init__('autonomous_flight_lidar')

        # QoS FIX
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self.offboard_pub = self.create_publisher(
            OffboardControlMode,
            '/fmu/in/offboard_control_mode', 10)

        self.traj_pub = self.create_publisher(
            TrajectorySetpoint,
            '/fmu/in/trajectory_setpoint', 10)

        self.cmd_pub = self.create_publisher(
            VehicleCommand,
            '/fmu/in/vehicle_command', 10)

        # Subscribers
        self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            qos)

        self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            qos)

        # Timer
        self.timer = self.create_timer(0.1, self.control_loop)

        # State
        self.counter = 0
        self.position = [0.0, 0.0, 0.0]
        self.lidar_data = None

        # Goal
        self.goal = np.array([20.0, 0.0])

        # Flags
        self.armed = False
        self.offboard_enabled = False

    # ----------------------------
    # ODOM CALLBACK
    # ----------------------------
    def odom_callback(self, msg):
        self.position = list(msg.position)

    # ----------------------------
    # LIDAR CALLBACK
    # ----------------------------
    def lidar_callback(self, msg):
        self.lidar_data = np.array(msg.ranges)

    # ----------------------------
    # ARM
    # ----------------------------
    def arm(self):
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.command = VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM
        msg.param1 = 1.0
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        self.cmd_pub.publish(msg)
        self.get_logger().info("🚀 ARM SENT")

    # ----------------------------
    # OFFBOARD MODE
    # ----------------------------
    def set_offboard(self):
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.command = VehicleCommand.VEHICLE_CMD_DO_SET_MODE
        msg.param1 = 1.0
        msg.param2 = 6.0
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        self.cmd_pub.publish(msg)
        self.get_logger().info("🟢 OFFBOARD ENABLED")

    # ----------------------------
    # DECISION LOGIC
    # ----------------------------
    def compute_direction(self):

        # No LiDAR → move forward
        if self.lidar_data is None:
            return np.array([1.0, 0.0])

        # Remove invalid
        data = self.lidar_data[np.isfinite(self.lidar_data)]

        if len(data) == 0:
            return np.array([1.0, 0.0])

        # Regions
        front = np.concatenate((self.lidar_data[:20], self.lidar_data[-20:]))
        left = self.lidar_data[60:120]
        right = self.lidar_data[-120:-60]

        front = front[np.isfinite(front)]
        left = left[np.isfinite(left)]
        right = right[np.isfinite(right)]

        front_min = np.min(front) if len(front) > 0 else 10
        left_min = np.min(left) if len(left) > 0 else 10
        right_min = np.min(right) if len(right) > 0 else 10

        self.get_logger().info(
            f"📡 F:{front_min:.2f} L:{left_min:.2f} R:{right_min:.2f}")

        # 🚧 Obstacle avoidance
        if front_min < 2.0:
            self.get_logger().warn("🚧 OBSTACLE DETECTED")

            if left_min > right_min:
                return np.array([0.0, 1.0])
            else:
                return np.array([0.0, -1.0])

        # Move toward goal
        goal_vec = self.goal - np.array(self.position[:2])
        norm = np.linalg.norm(goal_vec)

        if norm < 0.1:
            return np.array([0.0, 0.0])

        return goal_vec / norm

    # ----------------------------
    # MAIN CONTROL LOOP
    # ----------------------------
    def control_loop(self):

        timestamp = int(self.get_clock().now().nanoseconds / 1000)

        # OFFBOARD heartbeat
        offboard = OffboardControlMode()
        offboard.timestamp = timestamp
        offboard.position = True
        self.offboard_pub.publish(offboard)

        traj = TrajectorySetpoint()
        traj.timestamp = timestamp
        traj.yaw = 0.0

        self.get_logger().info(f"📍 POS: {self.position}")

        # Takeoff phase
        if self.counter < 50:
            traj.position = [0.0, 0.0, -3.0]

        # Enable OFFBOARD
        elif self.counter == 60 and not self.offboard_enabled:
            self.set_offboard()
            self.offboard_enabled = True

        # Arm
        elif self.counter == 70 and not self.armed:
            self.arm()
            self.armed = True

        # Navigation
        else:
            direction = self.compute_direction()

            speed = 2.0  # 🔥 STRONG MOTION

            new_x = self.position[0] + direction[0] * speed
            new_y = self.position[1] + direction[1] * speed

            self.get_logger().info(f"➡️ DIR: {direction}")

            traj.position = [new_x, new_y, -3.0]

        self.traj_pub.publish(traj)
        self.counter += 1


def main():
    rclpy.init()
    node = AutonomousFlight()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
