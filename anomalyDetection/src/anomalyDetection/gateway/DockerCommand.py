from .Command import Command
from .DockerExecutor import DockerExecutor

class DockerCommand(Command):

    def __init__(self, docker_command):
        self.docker_command = docker_command

    def execute(self):
        DockerExecutor.run_command(self.docker_command)
