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

def generate_launch_description():

    # Project paths
    world_pkg = get_package_share_directory('neo_gz_worlds')
    robot_description_pkg = get_package_share_directory('turtlebot3_gazebo')

    set_resource_path = SetEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        os.path.join(world_pkg, 'models')
    )

    # Load URDF of the robot
    urdf_file = os.path.join(robot_description_pkg, 'urdf', 'turtlebot3_waffle_pi.urdf')
    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

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
        arguments=[urdf_file],
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

    return LaunchDescription([
        set_resource_path,
        gz_sim,
        joint_state_publisher_gui,
        robot_state_publisher,
        spawn_entity
    ])