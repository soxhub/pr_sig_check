FROM python:3.9

COPY check_commits.py /check_commits.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["/check_commits.py"]