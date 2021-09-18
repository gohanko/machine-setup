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
    add_repository = manage_package.get('add_repository')
    if add_repository:
        for package_manager, repositories in add_repository.items():
            for repository in repositories:
                source = None
                if package_manager == 'flatpak':
                    source = repository.split(' ')[0]
                    repository = repository.split(' ')[1]

                unified_package_manager.add_repository(package_manager, repository, source)
    
    for package_manager, packages in manage_package.get('install').items():
        if package_manager == 'flatpak':
            for flatpak_source, flatpak_packages in packages.items():
                unified_package_manager.install(
                    package_manager,
                    flatpak_packages,
                    source=flatpak_source
                )
        else:
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
                if not os.path.exists(destination.parent):
                    os.makedirs(destination.parent)

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