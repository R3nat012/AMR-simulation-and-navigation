# AMR-simulation-and-navigation

Simulation of an AMR in different gz worlds using ros2 and nav2.

<img src="images/Exmpl1.png" alt="First simulation" width="400" height="400">

## Project overview

This ros2 pkg simulates a Turtlebot3 in a small warehouse in Gazebo fortress using ROS2 Humble distro. Nav2 was also used for the navigation stack of the AMR.

## System diagram

![Nodes and Topics graph](images/architecture.png)

## Prerequisites and dependencies

This project requires the following softwares:
 - Ubuntu 22.04
 - ROS 2 [Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
 - Gazebo [Fortress](https://gazebosim.org/docs/latest/ros_installation/)
 - Neobotix [repo](https://github.com/neobotix/neo_gz_worlds.git)
 - Turtlebot3 [repo](https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git)

## Installation instructions

1. Clone the repo
```bash
git clone https://github.com/R3nat012/AMR-simulation-and-navigation.git
```

2. Install dependencies
```bash
cd your_ws
rosdep install --from-paths src --ignore-src -r -y
```

3. Build the workspace
```bash
cd your_ws
colcon build
source install/setup.bash
```

4. (Work in progress) To use cartographer, we need to go to our world .sdf and paste the following lines inside the world definition

```xml
<plugin filename="libignition-gazebo-imu-system.so" name="ignition::gazebo::systems::Imu"/>
```

## Usage
Bringup the robot and the first world in gz

```bash
ros2 launch AMR-simulation-and-navigation amr_tes1.launch.py
```

To map our environment we have to use cartographer

```bash
ros2 launch AMR-simulation-and-navigation mapping.launch.py
```

In another terminal run rviz2
```bash
rviz2
```
To navigate with existing map we need to launch just the following file
```bash
ros2 launch AMR-simulation-and-navigation amr_navigation.launch.py
```
In another terminal run rviz2
```bash
rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz --ros-args -p use_sim_time:=true
```


## Project structure

```text
.
├── CMakeLists.txt
├── config
│   ├── my_map.pgm
│   ├── my_map.yaml
│   ├── nav2_params_amr.yaml
│   ├── server.config
│   └── tb3_cartographer.lua
├── images
│   ├── architecture.png
│   └── Exmpl1.png
├── include
│   └── amr_sim
├── launch
│   ├── amr_tes1.launch.py
│   ├── bringup.launch.py
│   └── mapping.launch.py
├── package.xml
├── README.md
├── src
└── urdf
    └── turtlebot3_gz_fortress.urdf

```

## Features and roadmap

Future updates and debugging:
 - Gazebo fortress world launch  [&#x2714;]
 - Spawn robot [&#x2714;]
 - Teleop [&#x2714;]
 - SLAM [&#x2714;]
 - Nav2 [&#x2714;]

## References

Credits to DYNAMIXEL and Neobotix 