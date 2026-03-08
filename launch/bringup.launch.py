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

    set_resource_path = SetEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        os.path.join(world_pkg, 'models')
    )

    gz_sim = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    ),
    launch_arguments={'gz_args': os.path.join(world_pkg, 'worlds', 'neo_workshop.sdf') + ' -r'}.items()
)
    return LaunchDescription([
        set_resource_path,
        gz_sim
    ])