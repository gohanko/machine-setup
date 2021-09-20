import shutil
import os
from colorama import Fore, Style
from machine_setup.common import run_command
from machine_setup.package_manager import GeneralPackageManager

class RecipeParser(object):
    def __init__(self, recipe):
        self.recipe = recipe
        self.general_package_manager = GeneralPackageManager()
    
    def _manage_package(self) -> None:
        manage_package = self.recipe.get('manage_package')

        add_repository = manage_package.get('add_repository')
        if add_repository:
            for package_manager, repositories in add_repository.items():
                for repository in repositories:
                    source = None
                    if package_manager == 'flatpak':
                        source = repository.split(' ')[0]
                        repository = repository.split(' ')[1]

                    self.general_package_manager.add_repository(package_manager, repository, source)
        
        for package_manager, packages in manage_package.get('install').items():
            if package_manager == 'flatpak':
                for flatpak_source, flatpak_packages in packages.items():
                    self.general_package_manager.install(
                        package_manager=package_manager,
                        package_list=flatpak_packages,
                        repository_name=flatpak_source
                    )
            else:
                self.general_package_manager.install(package_manager, packages)

    def _configure_package(self) -> None:
        print('{}Configuring the following applications:{}'.format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
        for application, configuration in self.recipe.get('configure_package').items():
            print('   -  {}'.format(application))
            files = configuration.get('files')
            if not files:
                continue

            source, destination = files.get('copy_from'), files.get('copy_to')
            if os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)

                shutil.copytree(source, destination)
            else:
                if not os.path.exists(destination.parent):
                    os.makedirs(destination.parent)

                shutil.copyfile(source, destination)
        

            if application == 'vscode' and configuration.get('install_extension'):
                for extension in configuration.get('install_extension'):
                    run_command(['code', '--install-extension', extension], shell=True)

    def run(self) -> None:
        self._manage_package()
        self._configure_package()