FROM python:3.11

WORKDIR /project

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH /project

USER 1000:1000
