FROM ubuntu:19.10

RUN apt update && \
    apt upgrade -y

RUN apt install -y git python3-pip python3-venv

RUN pip3 install flask virtualenv Flask

RUN git clone https://github.com/MarcAnthonyFanfan/webapp1

WORKDIR "/webapp1"

RUN python3 -m venv env

RUN . env/bin/activate

EXPOSE 5000

CMD ["/webapp1/start.sh"]