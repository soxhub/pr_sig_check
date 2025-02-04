FROM 691661262207.dkr.ecr.us-west-2.amazonaws.com/dkr-hub/library/python:3.9

COPY requirements.txt /requirements.txt
COPY check_commits.py /check_commits.py
COPY check_helpers /check_helpers

RUN pip install -r requirements.txt

ENTRYPOINT ["/check_commits.py"]
