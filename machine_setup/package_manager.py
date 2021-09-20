import re
import platform
import os
import ctypes
from colorama import Fore, Style
from machine_setup.common import run_command

SUPPORTED_PACKAGE_MANAGER = {
    'dnf': {
        'command': 'dnf',
        'install':  ['install'],
        'uninstall': 'remove',
        'assume_yes': '-y',
        'add_repo': ['config-manager', '--add-repo']
    },
    'flatpak': {
        'command': 'flatpak',
        'install': ['install', '--user'],
        'uninstall': 'uninstall',
        'assume_yes': '-y',
        'add_repo': ['remote-add', '--if-not-exists'],
    },
    'chocolatey': {
        'command': 'chocolatey',
        'install': ['install'],
        'uninstall': 'uninstall',
        'assume_yes': '-y'
    }
}

class GeneralPackageManager(object):
    def _is_elevated(self) -> bool:
        system = platform.system()
        if system == 'Windows':
            return ctypes.windll.shell32.IsUserAnAdmin()
        if system == 'Linux' or 'Darwin':
            return os.getuid() == 0

    def _flight_check(self) -> None:
        if not self._is_elevated():
            print('Please run the shell as an admin user!')
            exit(0)

    def add_repository(self, package_manager: str, repository_url: str, repository_name: str=None, assume_yes: bool=True) -> bool:
        self._flight_check()
        supported_package_manager = SUPPORTED_PACKAGE_MANAGER[package_manager]

        add_repository_command = [supported_package_manager.get('command'), *supported_package_manager.get('add_repo')]
        if assume_yes:
            add_repository_command.append(supported_package_manager.get('assume_yes'))
        if repository_name:
            add_repository_command.append(repository_name)

        add_repository_command.append(repository_url)
        return run_command(add_repository_command)

    def install(self, package_manager: str, package_list: list, repository_name: str=None, assume_yes: bool=True) -> tuple:
        self._flight_check()
        supported_package_manager = SUPPORTED_PACKAGE_MANAGER[package_manager]
        base_install_command = [supported_package_manager.get('command'), *supported_package_manager.get('install')]
        if repository_name:
            base_install_command.append(repository_name)
        if assume_yes:
            base_install_command.append(supported_package_manager.get('assume_yes'))

        print('{}Installing the following packages:{}'.format(Fore.CYAN, Style.RESET_ALL))
        success_counter = 0
        for package in package_list:
            color, symbol = '', ''
            
            status = run_command([*base_install_command, package])
            if status[0]:
                success_counter += 1

                regex = re.compile('already installed')
                if regex.search(status[1]):
                    color = Fore.LIGHTBLACK_EX
                    symbol = '-'
                else:
                    color = Fore.GREEN
                    symbol = '√'
            else:
                color = Fore.RED
                symbol = 'X'

            print('  {}[{}]{} {}'.format(color, symbol, Style.RESET_ALL, package))

        return (success_counter, len(package_list))

    def uninstall(self, package_manager: str, package_list: list, repository_name: str=None, assume_yes: bool=True) -> tuple:
        self._flight_check()
        supported_package_manager = SUPPORTED_PACKAGE_MANAGER[package_manager]
        base_uninstall_command = [supported_package_manager.get('commend'), supported_package_manager.get('uninstall')]
        if assume_yes:
            base_uninstall_command.append(supported_package_manager.get('assume_yes'))
        if repository_name:
            base_uninstall_command.append(repository_name)

        print('{}Removing the following packages:{}'.format(Fore.CYAN, Style.RESET_ALL))
        success_counter = 0
        for package in package_list:
            color, symbol = '', ''
            
            status = run_command([*base_uninstall_command, package])
            if status[0]:
                success_counter += 1

                color = Fore.GREEN
                symbol = '√'
            else:
                color = Fore.RED
                symbol = 'X'

            print('    {}[{}]{} {}'.format(color, symbol, Style.RESET_ALL, package))

        return (success_counter, len(package_list))