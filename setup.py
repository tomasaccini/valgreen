from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='valgreen',
    version='0.4',
    description='Valgrind output readable for human beings ',
    long_description=readme(),
    url='https://github.com/tomasaccini/valgreen/',
    author='TomasAccini, FdelMazo',
    scripts=['valgreen'],     
    packages=['Beautifier'],
    install_requires=['colorama'], 
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
