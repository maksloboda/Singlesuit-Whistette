FROM python:slim-buster

RUN mkdir Solver

WORKDIR Solver

ENV PYTHONPATH=./legacy

COPY ./ ./

CMD ["python", "tests.py"]