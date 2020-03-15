[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![](https://github.com/Software-Natives-OSS/cicd_sim/workflows/Python%20package/badge.svg)
![](https://codecov.io/gh/Software-Natives-OSS/cicd_sim/graph/badge.svg)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Software-Natives-OSS/cicd_sim/master?filepath=notebooks)

# CI/CD Simulator

In continuous integration (CI), versioning plays an important role. This project was created to make versioning of Conan artifacts tangible. It does so by letting the user create a virtual infrastructure of

- Git repositories (e.g. GitHub)
- Buildmaschine (e.g. Jenkins)
- Artifact store (e.g. Artifactory)
- Conan

Within this environment, the user can safely and effortlessly test what happens if versions are use the one or the other way.

This project is implemented in Python 3.

## Introduction

Conan package versioning follows [semver.org](https://semver.org). While semver specifies all aspects of versioning it also provides lots of flexibility how excatly to put it into praxis. That makes it not fully obvious how to effectively apply versions to your Conan packages:

- Should I use pre-release tags and how
- Should I use build numbers and how
- Should I include the git SHA in the package name and how
- How do the above influence package selection on consumer side (i.e. `conan install`)?
- ...

Finding the right answers is not an easy task and it's helpful (if not required) to conduct some experiments. But conducting such experiments is another not so trivial task because it involves quite some infrastructure: Git repos (e.g. GitHub/GitLab/Bitbucket), a buildmachine (e.g. Jenkins), an artifact store (e.g. Artifactory), ...

That's where this `CICD Simulator` comes in: It allows you to create a virtual "environment" with git repos, branches a buildmachine and an artifactory. Everything fully virtual in the RAM. It allows harmless, super fast experiments with different versioning approaches for your libraries' and projects' artifacts.

## Quick start Jupyter Notebooks

Choose one of these:

### Binder

By far the easiest way to run the simulator is by clicking the Binder batch. This starts Binder which may take up to ~5 mins.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Software-Natives-OSS/cicd_sim/master?filepath=notebooks)

### Docker

Quick start guide to run this project on your Desktop system. In the current directory, execute:

```sh
docker build -f docker/Dockerfile -t cicd-sim .
docker run --rm \
    -p 8888:8888 \
    -v "$(pwd)/notebooks:/home/jovyan"\
    cicd-sim

```

Check the output click the link and start playing!

### Python

Install required libraries, install this `cdcd_sim` module and finally run Jupyter on the example notebook

```sh
pip3 install -r requirements.txt
python3 setup.py install
jupyter notebook notebooks

```

## Todo

- Artifact versioning strategy is currently hardcoded in the 'Jenkins' implementation. Make this behavior easily adjustable by the user of the simulator
- Support multiple `requires`: Right now, each project can only reference zero or one requires

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage information on PyScaffold see https://pyscaffold.org/.
