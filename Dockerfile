FROM jupyter/minimal-notebook

# install Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

# COPY src /tmp/src
# COPY setup.py README.md /tmp/
# RUN find /tmp -type f
# RUN cd /tmp \
#     && python /tmp/setup.py bdist_wheel
# RUN python -m pip install /tmp/cicd_simulator-0.1-py2-none-any.whl
