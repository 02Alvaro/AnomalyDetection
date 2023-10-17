import subprocess

class DockerExecutor:

    @staticmethod
    def execute(docker_command):
        result = subprocess.run(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result
