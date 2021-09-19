import os
import shutil
import ctypes
import platform
import subprocess
from machine_setup.exceptions import NotInstalledException

SUPPORTED_PACKAGE_MANAGER = {
    'dnf': {
        'command': 'dnf',
        'install': 'install',
        'uninstall': 'remove',
        'assume_yes': '-y',
        'add_repo': ['config-manager', '--add-repo']
    },
    'flatpak': {
        'command': 'flatpak',
        'install': 'install',
        'uninstall': 'uninstall',
        'assume_yes': '-y',
        'add_repo': ['remote-add', '--if-not-exists'],
    },
    'chocolatey': {
        'command': 'chocolatey',
        'install': 'install',
        'uninstall': 'uninstall',
        'assume_yes': '-y'
    }
}

class UnifiedPackageManager(object):
    def _is_elevated(self) -> bool:
        if platform.system() == 'Windows':
            return ctypes.windll.shell32.IsUserAnAdmin()
        elif platform.system() == 'Linux': # possibly macos as well
            return os.getuid() == 0

    def _flight_check(self, package_manager: str) -> dict:

        if shutil.which(package_manager) is None:
            raise NotInstalledException

        return SUPPORTED_PACKAGE_MANAGER[package_manager]

    def add_repository(self, package_manager: str, repository: str, source: str) -> None:
        package_manager = self._flight_check(package_manager)
        add_repository_command = [
            package_manager.get('command'),
            *package_manager.get('add_repo'),
        ]

        if source:
            add_repository_command.append(source)
        add_repository_command.append(repository)

        subprocess.run(add_repository_command)

    def install(self, package_manager: str, package_list: list, source: str = None, assume_yes: bool = True) -> None:
        package_manager = self._flight_check(package_manager)
        install_command = [
            package_manager.get('command'), 
            package_manager.get('install'),
        ]

        if source:
            install_command.append(source)
        
        install_command = install_command + package_list
        if assume_yes:
            install_command.append(package_manager.get('assume_yes'))

        subprocess.run(install_command)

    def uninstall(self, package_manager: str, package_list: list, assume_yes: bool=True) -> None:
        package_manager = self._verify(package_manager)
        
        uninstall_command = [
            package_manager.get('command'),
            package_manager.get('uninstall'),
            *package_list,
        ]
    
        if assume_yes:
            uninstall_command.append(package_manager.get('assume_yes'))

        subprocess.run(uninstall_command)