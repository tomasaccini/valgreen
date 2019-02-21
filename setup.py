from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='valgreen',
    version='0.1',
    description='Valgrind output readable for human beings ',
    long_description=readme(),
    url='https://github.com/tomasaccini/Valgreen/',
    author='TomasAccini, FdelMazo',
    scripts=['valgreen'],     
    install_requires=['colorama'], 
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
