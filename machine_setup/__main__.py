import argparse
import os
import shutil
import subprocess
from pathlib import Path
from yaml import load, Loader
from machine_setup.unified_package_manager import UnifiedPackageManager

def load_yaml(file: str) -> dict:
    file = Path(file)
    with open(file, 'r') as file_handler:
        data = load(file_handler, Loader=Loader)

    # Replace relative path in data with proper path.
    for conf in data.get('configure_package').values():
        conf['files']['copy_from'] = Path(file.parent.absolute(), conf['files']['copy_from'])
        conf['files']['copy_to'] = Path(conf['files']['copy_to'])

    return data

def install_vscode_extensions(extensions: list) -> None:
    for extension in extensions:
        subprocess.run(['code', '--install-extension', extension], shell=True)

def recipe_interpreter(recipe: str) -> None:
    unified_package_manager = UnifiedPackageManager()

    manage_package = recipe.get('manage_package')
    if manage_package.get('install_chocolatey'):
        unified_package_manager.install_chocolatey()
    
    add_repository = manage_package.get('add_repository')
    if add_repository:
        for package_manager, repositories in add_repository.items():
            for repository in repositories:
                unified_package_manager.add_repository(package_manager, repository)
    
    for package_manager, packages in manage_package.get('install').items():
        unified_package_manager.install(package_manager, packages)

    configure_package = recipe.get('configure_package')
    for application, configuration in configure_package.items():
        files = configuration.get('files')
        if files:
            source = files.get('copy_from')
            destination = files.get('copy_to')

            if os.path.isdir(files.get('copy_from')):
                if os.path.exists(destination):
                    print('Removing existing configuration folder at {}'.format(destination))
                    shutil.rmtree(destination)
    
                print('Copying configuration folder from {} to {}'.format(source, destination))
                shutil.copytree(source, destination)
            else:
                print('Copying configuration file from {} to {}'.format(source, destination))
                shutil.copyfile(source, destination)

        if application == 'vscode' and configuration.get('install_extension'):
            install_vscode_extensions(configuration.get('install_extension'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipe', help='Recipe/Instructions for setting up your machine.')

    args = parser.parse_args()
    if args.recipe:
        recipe = load_yaml(args.recipe)
        recipe_interpreter(recipe)