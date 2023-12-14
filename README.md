# Wind Correction

## Instalation

If you don't have it yet, install [Poetry](https://python-poetry.org/docs/)

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```


### Repository Setup

```bash
$ git clone git@gitlab.com:academic-aviation-club/droniada-2024/wind-correction.git
$ cd wind-correction
$ poetry shell
$ poetry install --no-root
```

## Checking Code Quality

```bash
$ task formatting
$ task flake8
$ task mypy
$ task pylint
```

## Instruction for Windows users

Read this [installation guide](https://docs.fedoraproject.org/en-US/fedora/latest/getting-started/)

https://pyscard.sourceforge.io/pyscard-framework.html#framework-samples