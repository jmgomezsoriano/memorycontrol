from setuptools import setup, find_packages

setup(
    name='memorycontrol',
    version='0.0.1',
    description='A resource monitor with auto-shutdown for processes',
    author='Your Name',
    author_email='youremail@example.com',
    url='https://github.com/yourusername/memorycontrol',
    packages=find_packages(),
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
