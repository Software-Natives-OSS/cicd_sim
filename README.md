# CI/CD Simulator

In continuous integration (CI), versioning plays an important role. This project was created to make versioning of Conan artifacts tangible. Implemented in Python 3

## Introduction

Conan package versioning follows [semver.org](https://semver.org). While semver specifies all aspects of versioning it also provides lots of flexibility. That makes it not fully obvious how to effectively apply versions to your Conan packages:

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

Just click here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Software-Natives-OSS/cicd_sim.git/master)

### Docker

Quick start guide to run this project on your Desktop system. In the current directory, execute:

```sh
docker build -t cicd-sim .
docker run --rm \
    -p 8888:8888 \
    -v "$(pwd)/src:/home/jovyan"\
    cicd-sim

```

Check the output click the link and start playing!

### Python

```sh
pip3 install -r requirements.txt
jupyter notebook src

```

## Todo

- Artifact versioning strategy is currently hardcoded in the 'Jenkins' implementation. Make this behavior easily adjustable by the user of the simulator
- Support multiple `requires`: Right now, each project can only reference zero or one requires

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage information on PyScaffold see https://pyscaffold.org/.
