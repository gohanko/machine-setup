import setuptools

with open('README.md', 'r') as file_handler:
    long_description = file_handler.read()

package_list = []
with open('requirements.txt', 'r') as file_handler:
    package_list = file_handler.readlines()

setuptools.setup(
    name='machine_setup',
    version='0.0.1',
    author='Yii Kuo Chong',
    author_email='26451183+gohanko@users.noreply.github.com',
    description='Simple CLI tool for automatically setting up your personal/work machines.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gohanko/machine-setup',
    packages=setuptools.find_packages(include=['machine_setup', 'machine_setup.*']),
    install_requires=package_list,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)