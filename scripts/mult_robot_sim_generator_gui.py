
from launch_file_constructor import LaunchFileConstructor

class MultiRobotSimGenerator(object):
    def __init__(self, launch_file_constructor: LaunchFileConstructor):
        self._lf_constructor = launch_file_constructor