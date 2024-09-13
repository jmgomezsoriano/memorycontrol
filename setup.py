from setuptools import setup, find_packages

setup(
    name='memorycontrol',
    version='0.1.0',
    description='A resource monitor with auto-shutdown for processes',
    author='Your Name',
    author_email='youremail@example.com',
    url='https://github.com/yourusername/memorycontrol',
    packages=find_packages(),
    install_requires=[
        'psutil',  # Add the core dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
