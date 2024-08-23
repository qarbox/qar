from setuptools import setup

setup(
    name='qar',
    version='1.0',
    description='qar',
    author='Edward Thatch',
    author_email='edwardqar@protonmail.com',
    url='https://github.com/qarbox/qar',
    packages=['qar'],
    install_requires=['docker', 'zeroconf', '1337x'],
    entry_points={
        'console_scripts': [
            'qar = qar.cli:compose',
        ],
    },
)