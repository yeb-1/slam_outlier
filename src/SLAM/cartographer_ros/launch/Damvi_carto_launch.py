import os
from datetime import datetime

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    script_path = os.path.abspath(__file__)
    main_dir = os.path.dirname(script_path)
    package_dir = os.path.dirname(main_dir)
    config_dir = os.path.join(package_dir, 'configuration_files')
    workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(package_dir)))
    score_distribution_dir = os.path.join(
        workspace_dir, 'global_constraint_score_distributions')
    os.makedirs(score_distribution_dir, exist_ok=True)
    score_distribution_csv_path = os.path.join(
        score_distribution_dir,
        f"fast_correlative_score_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    )
    return LaunchDescription([
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            additional_env={
                'FAST_CORRELATIVE_SCORE_DISTRIBUTION_CSV_PATH':
                    score_distribution_csv_path,
            },
            parameters=[{'use_sim_time': True}],
            arguments = [
                '-configuration_directory', config_dir,
                '-configuration_basename', 'Damvi_carto_config.lua'],
            remappings=[
                ('scan', 'scan'),
                ('imu', 'imu/data'),
                ('tf', 'tf'),
                ('tf_static', 'tf_static'),
            ],
        ),

        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': True, 'resolution': 0.05}],
            remappings=[
                ('map', 'map'),
                ('occupancy_grid', 'map'),
            ],
        ),

        Node(
            package='cartographer_ros',
            executable='trajectory_to_odom',
            name='trajectory_to_odom',
            output='screen',
            parameters=[{'use_sim_time': True}],
        )
    ])
