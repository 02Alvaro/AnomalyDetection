import subprocess

class DockerExecutor:

    @staticmethod
    def run_command(docker_command):
        result = subprocess.run(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result
