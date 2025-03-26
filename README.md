# twitter_etl_pipeline
An end-to-end data engineering project involving extracting data using the Twitter API, utilizing the python pandas library to transform data, and dagster for orchestration.

## Getting started

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.


### Unit testing

Tests are in the `twitter_etl_pipeline_tests` directory and you can run tests using `pytest`:

```bash
python -m pytest twitter_etl_pipeline_tests
```

### Schedules and sensors

#TODO add schedule

