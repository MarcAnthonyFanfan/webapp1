FROM ubuntu:19.10

RUN apt update && \
    apt upgrade -y

RUN apt install -y git python3-pip python3-venv libmysqlclient-dev build-essential libssl-dev libffi-dev python3-dev

RUN pip3 install flask virtualenv Flask wheel flask_mysqldb pyopenssl

RUN git clone https://github.com/MarcAnthonyFanfan/webapp1

WORKDIR "/webapp1"

RUN python3 -m venv env

RUN . env/bin/activate

EXPOSE 5000

RUN chmod +x ./start.sh

ENV FLASK_APP=webapp1