import subprocess
from pathlib import Path
from yaml import load, Loader

def run_command(command: str, shell: bool=False) -> tuple:
    try:
        output = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            shell=shell
        )

        return (True, output.stdout)
    except subprocess.CalledProcessError:
        return (False, None)

def load_yaml(file: str) -> dict:
    file = Path(file)
    with open(file, 'r') as file_handler:
        data = load(file_handler, Loader=Loader)

    # Replace relative path in data with proper path.
    for conf in data.get('configure_package').values():
        conf['files']['copy_from'] = Path(file.parent.absolute(), conf['files']['copy_from'])
        conf['files']['copy_to'] = Path(conf['files']['copy_to'])

    return data