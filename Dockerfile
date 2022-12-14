FROM python:3.9

COPY requirements.txt /requirements.txt
COPY check_commits.py /check_commits.py
COPY check_helpers /check_helpers

RUN pip install -r requirements.txt

ENTRYPOINT ["/check_commits.py"]