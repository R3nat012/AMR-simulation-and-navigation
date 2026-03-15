from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('amr_sim'),'config')
    map_file = os.path.join(config_dir,'my_map.yaml')
    params_file = os.path.join(config_dir,'nav2_params_amr.yaml')
    return LaunchDescription([

    # Bringing our Robot
    IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('amr_sim'),'/launch','/amr_tes1.launch.py'])
    ),
    # Integerating Nav2 Stack
    IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('nav2_bringup'),'/launch','/bringup_launch.py']),
        launch_arguments={
        'map':map_file,
        'params_file': params_file,
        'use_sim_time': 'true'}.items(),

    ),

    ])