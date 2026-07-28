# Kortex Servo Simulation for Kinova Gen3 Lite

This package provides a servo node interface for the Kinova Gen3 Lite robotic arm using ROS 2 Jazzy and MoveIt 2 Servo. It allows you to control the robot in simulation (and real hardware) using Twist commands in Gazebo.

## Usage

**Terminal 1: Launch the Servo Node**

This launch file starts the MoveIt Servo node.

```bash
ros2 launch kortex_servo_simulation servo.launch.py
```

## Example: Move the Robotic Arm using Keyboard Teleop

**Terminal 2: Run the Keyboard Example**

Start the standard ROS 2 keyboard teleoperation node:

```bash
ros2 launch kortex_servo_simulation keyboard_example.launch.py
```

Use the flowing keys to control the robot:

Movement (Hold down):
w: +Z (Up)
s: -Z (Down)
a: -Y (Left)
d: +Y (Right)

Speed:
q: Increase speed (x1.1)
e: Decrease speed (x0.9)

## Configuration

The MoveIt Servo parameters are defined in `config/servo_config.yaml`. It includes configurations for collision checking, command scaling, and singularity thresholds to prevent sudden stops when the arm approaches its kinematic limits.
