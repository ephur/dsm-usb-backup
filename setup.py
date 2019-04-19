from setuptools import setup, find_packages

setup(
    name='dsmusbbackup',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'click>=7'
    ],
    entry_points={
        'console_scripts': [
            'dsmusbbackup=dsmusbbackup.cli:main'
        ]
    },
    setup_requires=[
        "flake8"
    ]
)
