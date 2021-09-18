import setuptools

with open('README.md', 'r', encoding='UTF-8') as fh:
    long_description = fh.read()

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
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)