from setuptools import setup, find_packages

setup(
    name="waze_home",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "requests>=2.28.0",
        "rich>=12.0.0",
        "python-dotenv>=0.20.0",
        "WazeRouteCalculator>=0.15.0",
    ],
    entry_points={
        "console_scripts": [
            "waze-home=waze_home.cli:cli",
        ],
    },
    python_requires=">=3.10",
)