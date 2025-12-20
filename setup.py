from setuptools import setup, find_packages

setup(
    name="smartapi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.18.4",
        "six>=1.11.0",
        "python-dateutil>=2.6.1",
        "websocket-client>=0.46.0"
    ],
)