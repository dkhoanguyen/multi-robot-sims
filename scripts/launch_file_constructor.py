
from io import TextIOWrapper

class LaunchFileConstructor(object):
    def __init__(self, package_name: str, launch_file_name: str):
        self._package_name = package_name
        self._launch_file_name = launch_file_name + '.launch'
        # TODO: Remove this hardcoded line in the future
        self._launch_dir = '/home/khoa/multi_robot_ws/src/multi_turtlebot3_sims/launch/'
        self._launch_file_path = self._launch_dir + self._launch_file_name

        self._world_arg = {}
        self._robots_arg = []

    def prepare_world(self):
        pass

    def write_world_to_file(self, lf: TextIOWrapper, package_name: str, world_path: str):
        # TODO: This should not be hardcoded
        lf.write('<!-- Spawn World -->\n')
        lf.write('<include file="$(find gazebo_ros)/launch/empty_world.launch">\n')
        lf.write(f'<arg name="world_name" value="$(find {package_name}){world_path}" />\n')
        lf.write('<arg name="paused" value="false" />\n')
        lf.write('<arg name="use_sim_time" value="true" />\n')
        lf.write('<arg name="gui" value="true" />\n')
        lf.write('<arg name="headless" value="false" />\n')
        lf.write('<arg name="debug" value="false" />\n')
        lf.write('</include>\n')

    def set_robot_infos(self, robot_infos: list):
        for indx, robot_info in enumerate(robot_infos):
            self.prepare_robots(indx,robot_info)

    def prepare_robots(self, idx: int, robot_info: dict):
        robot_arg = {}
        robot_arg[f'robot_{idx}_name'] = robot_info['name']
        robot_arg[f'robot_{idx}_x'] = robot_info['x']
        robot_arg[f'robot_{idx}_y'] = robot_info['y']
        robot_arg[f'robot_{idx}_z'] = robot_info['z']
        robot_arg[f'robot_{idx}_yaw'] = robot_info['yaw']
        robot_arg[f'robot_{idx}_description_package'] = robot_info['robot_description_package']
        robot_arg[f'robot_{idx}_description_model_path'] = robot_info['robot_description_model_path']
        self._robots_arg.append(robot_arg)

    def _write_indv_robot_to_file(self, lf: TextIOWrapper, robot_id: int, robot_info: dict):
        lf.write(f'<!-- Spawn Robot {robot_id} -->\n')
        # Prepare the arguments
        for key, value in robot_info.items():
            lf.write(f'<arg name="{key}" default="{value}" />\n')
        lf.write('\n')
        # Prepare the nodes
        lf.write(f'<group ns="$(arg robot_{robot_id}_name)">\n')
        
        # Robot description model path
        lf.write(('<param name="robot_description" command="$(find xacro)/xacro --inorder '
        f'$(find {robot_info[f"robot_{robot_id}_description_package"]})'
        f'{robot_info[f"robot_{robot_id}_description_model_path"]}" />\n'))

        # Robot state publisher
        lf.write(f'<node pkg="robot_state_publisher" type="robot_state_publisher" name="robot_state_publisher" output="screen"> '
        f'<param name="publish_frequency" type="double" value="50.0" />'
        f'<param name="tf_prefix" value="$(arg robot_{robot_id}_name)" />'
        '</node>')

        # Robot urdf spawner
        lf.write('<node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model" args="-urdf '
        f'-model $(arg robot_{robot_id}_name) '
        f'-x $(arg robot_{robot_id}_x) '
        f'-y $(arg robot_{robot_id}_y) '
        f'-z $(arg robot_{robot_id}_z) '
        f'-Y $(arg robot_{robot_id}_yaw) '
        f'-param robot_description" />\n')

        # Close group
        lf.write('</group>\n')

    def write_robots_to_file(self, lf: TextIOWrapper):
        for idx, robot_info in enumerate(self._robots_arg):
            self._write_indv_robot_to_file(lf, idx, robot_info)
            lf.write('\n')

    def construct(self):
        with open(self._launch_file_path, 'w') as lf:
            lf.write('<launch>\n')
            self.write_world_to_file(lf,'turtlebot3_gazebo','/worlds/empty.world')
            lf.write('\n')
            self.write_robots_to_file(lf)
            lf.write('</launch>\n')


robot1_info = {
    'name': 'tb3_0',
    'x': 0.0,
    'y': 0.0,
    'z': 0.0,
    'yaw': 1.57,
    'robot_description_package': 'turtlebot3_description',
    'robot_description_model_path': '/urdf/turtlebot3_burger.urdf.xacro'
}

robot2_info = {
    'name': 'tb3_1',
    'x': 0.0,
    'y': 1.0,
    'z': 0.0,
    'yaw': 1.57,
    'robot_description_package': 'turtlebot3_description',
    'robot_description_model_path': '/urdf/turtlebot3_burger.urdf.xacro'
}

robots_info = [robot1_info,robot2_info]
test = LaunchFileConstructor('multi_turtlebot3_sims','test')
test.set_robot_infos(robots_info)
test.construct()
