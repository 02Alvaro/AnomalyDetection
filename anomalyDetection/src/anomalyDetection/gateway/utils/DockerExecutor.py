import subprocess

class DockerExecutor:

    @staticmethod
    def execute(docker_command):
        result = subprocess.run(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        stdout_lines = result.stdout.splitlines()
        stderr_lines = result.stderr.splitlines()

        for line in stdout_lines:
            print(f"[Algorithm] {line}")

        for line in stderr_lines:
            print(f"[AlgorithmError] {line}")

        return result
