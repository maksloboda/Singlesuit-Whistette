FROM python:slim-buster

RUN mkdir Solver

WORKDIR Solver

COPY ./ ./

CMD ["python", "tests.py"]