import subprocess


class DockerExecutor:
    @staticmethod
    def execute(docker_command):
        try:
            result = subprocess.run(
                docker_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            stdout_lines = result.stdout.splitlines()

            for line in stdout_lines:
                print(f"[Algorithm] {line}")

        except subprocess.CalledProcessError as e:
            stderr_lines = e.stderr.splitlines()
            for line in stderr_lines:
                print(f"[AlgorithmError] {line}")

            raise RuntimeError("Failed to execute docker command") from e
