FROM python:3.8

ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1

RUN mkdir /app

RUN apt -y update && apt -y upgrade

RUN apt -y install nano

RUN apt -y install locales locales-all && locale-gen en_US.UTF-8 ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LANGUAGE=ru_RU:ru

ADD reqs.txt /app/src/

# use cache
RUN python3 -m pip install -r /app/src/reqs.txt -U

ADD . /app/src/

# don't use cache
RUN python3 -m pip install -r /app/src/reqs.txt -U

WORKDIR /app/src

EXPOSE 80
