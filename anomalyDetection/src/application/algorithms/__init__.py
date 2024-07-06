import importlib
from pathlib import Path

try:
    # Obtén la ruta actual del paquete
    current_dir = Path(__file__).parent

    # Recorre todos los archivos Python en el directorio (excluyendo __init__.py)
    for file in current_dir.glob("**/*.py"):
        if file.name != "__init__.py" and not file.name.startswith("__") and not file.name.__contains__("src"):
            # Crea el nombre del módulo Python para la importación
            module_relative_path = file.relative_to(current_dir.parent)
            module_name = (
                str(module_relative_path)
                .replace("/", ".")
                .replace("\\", ".")
                .rstrip(".py")
            )

            # Importa el módulo
            importlib.import_module(f"application.{module_name}")
except Exception as e:
    raise Exception(f"{module_name}")
