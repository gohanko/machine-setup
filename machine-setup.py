import ctypes
import os
import platform
import subprocess
import shutil
from pathlib import Path

def install_chocolatey_packages():
    subprocess.run(['Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\')) -y'], shell=True)

    with open('packages/chocolatey.txt') as file_handler:
        packages = file_handler.read().replace('\n', ' ')

    subprocess.run('choco install {} -y'.format(packages))

def install_configuration_files(platform):
    CONFIG_METADATA = {
        'firefox': {
            'source': Path('./configurations/firefox/distribution/'),
            'destination': {
                'Windows': Path('C:\\Program Files\\Mozilla Firefox\\distribution\\')
            }
        },
        'vscode': {
            'source': Path('./configurations/vscode/settings.json'),
            'destination': {
                'Windows': Path('%APPDATA%\\Code\\User\\settings.json'),
                'Linux': Path('$HOME/.config/Code/User/settings.json')
            }
        }
    }

    for program in CONFIG_METADATA.keys():
        source = CONFIG_METADATA[program]['source']
        destination = CONFIG_METADATA[program]['destination'][platform]
        if os.path.isdir(source):
            print('Copying configuration folder from {} to {}'.format(source, destination))
            shutil.copytree(source, destination)
        else:
            print('Copying configuration file from {} to {}'.format(source, destination))
            shutil.copyfile(source, destination)

def install_vscode_extensions():
    with open('configurations/vscode/extensions.txt') as file_handler:
        for extension in file_handler.readlines():
            print('Installing VSCode extension: {}'.format(extension))
            subprocess.run(['code', '--install-extension', extension], shell=True)

if __name__ == '__main__':
    platform = platform.system()

    if platform == 'Windows':
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print('Please run the shell as an admin user!')
            exit(0)

        install_chocolatey_packages()
        install_vscode_extensions()
        install_configuration_files()
