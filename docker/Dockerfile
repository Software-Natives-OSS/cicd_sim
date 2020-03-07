FROM jupyter/minimal-notebook

COPY . /tmp/cicd_sim

# seems to be required for `python setup.py ...`
USER root
RUN cd /tmp/cicd_sim && python setup.py bdist_wheel && python -m pip install dist/*.whl && rm -rf *

# undo user change
USER jovyan
