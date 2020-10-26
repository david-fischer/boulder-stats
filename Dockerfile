FROM python:3

ADD . boulder-stats

WORKDIR boulder-stats

RUN pip install .

ENTRYPOINT [ "boulder_stats" ]
