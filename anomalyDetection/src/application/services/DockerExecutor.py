import subprocess

class DockerExecutor:
    @staticmethod
    def execute(docker_command):
        try:
            with subprocess.Popen(
                docker_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as process:

                # Procesar stdout en tiempo real
                for stdout_line in iter(process.stdout.readline, ""):
                    print(f"[Algorithm] {stdout_line}", end="")

                # Esperar a que el proceso termine y obtener el código de salida
                process.wait()

                # Procesar stderr después de que el proceso haya terminado
                # Esto es solo si necesitas procesar los errores después
                stderr_lines = process.stderr.read().splitlines()
                for line in stderr_lines:
                    print(f"[AlgorithmError] {line}")

                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, docker_command)

        except subprocess.CalledProcessError as e:
            print(f"Failed to execute docker command, error code: {e.returncode}")
            raise RuntimeError("Failed to execute docker command") from e
