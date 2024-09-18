import glob
from shutil import rmtree

from setuptools import setup, find_packages, Command

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CleanCommand(Command):
    """ Custom clean command to tidy up the project root. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rmtree('build', ignore_errors=True)
        rmtree('dist', ignore_errors=True)
        for file in glob.glob('*.egg-info'):
            rmtree(file)


setup(
    cmdclass={'clean': CleanCommand},
    name='memorycontrol',
    version='0.0.2',
    description='A resource monitor with auto-shutdown for processes',
    license='GPL v3',
    author='Álex Muñoz Pérez and José M. Gómez',
    author_email='jmgomez.soriano@gmail.com',
    url='https://github.com/jmgomezsoriano/memorycontrol',
    packages=find_packages(exclude=["test"]),
    package_dir={'memorycontrol': 'memorycontrol'},
    install_requires=[
        'psutil==6.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'memorycontrol=memorycontrol.__main__:main'
        ]
    }
)
