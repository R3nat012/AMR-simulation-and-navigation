#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable
import xacro

def generate_launch_description():

    # Project paths
    world_pkg = get_package_share_directory('neo_gz_worlds')
    xacro_file = os.path.join(get_package_share_directory('amr_sim'), 'urdf', 'turtlebot3_gz_fortress.urdf')

    set_resource_path = SetEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        os.path.join(world_pkg, 'models')
    )

    # Load URDF of the robot
    robot_description = xacro.process_file(xacro_file).toxml()
    turtlebot3_gazebo_pkg = get_package_share_directory('turtlebot3_gazebo')

    set_resource_path = SetEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        ':'.join([
            os.path.join(world_pkg, 'models'),
            os.path.dirname(turtlebot3_gazebo_pkg),
            os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
        ])
    )

    # Spawn the world
    gz_sim = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    ),
    launch_arguments={'gz_args': os.path.join(world_pkg, 'worlds', 'neo_workshop.sdf') + ' -r'}.items()
    )

    # Configure the joints of the robot
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        arguments=[xacro_file],
        output=['screen']
    )

    # Configure the robot state
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time: True'},
            {'robot_description': robot_description},
        ]
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'turtlebot3',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '1.0',
            '-Y', '1.57',  # yaw rotation in radians
        ],
        output='screen'
    )

    # Bridge between gz topics and ros2
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry',
            '/world/default/model/turtlebot3/link/base_footprint/sensor/lidar/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            '/world/default/model/turtlebot3/link/base_footprint/sensor/camera/image@sensor_msgs/msg/Image[ignition.msgs.Image',
            '/world/default/pose/info@sensor_msgs/msg/Imu[ignition.msgs.IMU'
        ],
        remappings=[
            ('/world/default/model/turtlebot3/link/base_footprint/sensor/lidar/scan', '/scan'),
            ('/world/default/model/turtlebot3/link/base_footprint/sensor/camera/image', '/camera/image'),
            ('/world/default/pose/info', '/imu')
        ],
        output='screen'
    )

    # Load the sensor plugins
    set_server_config = SetEnvironmentVariable(
        'IGN_GAZEBO_SERVER_CONFIG',
        os.path.join(get_package_share_directory('amr_sim'), 'config', 'server.config')
    )

    return LaunchDescription([
        set_server_config,
        set_resource_path,
        gz_sim,
        joint_state_publisher_gui,
        robot_state_publisher,
        spawn_entity,
        bridge
    ])