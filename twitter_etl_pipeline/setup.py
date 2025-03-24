from setuptools import find_packages, setup

setup(
    name="twitter_etl_pipeline",
    packages=find_packages(exclude=["twitter_etl_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
