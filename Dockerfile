FROM ubuntu:19.10

RUN apt update && \
    apt upgrade -y

RUN apt install -y git python3-pip 

RUN pip3 install flask virtualenv Flask

RUN git clone https://github.com/MarcAnthonyFanfan/webapp1

WORKDIR "/webapp1"

RUN git reset --hard HEAD

RUN git pull

RUN python3 -m venv env

RUN source env/bin/activate

RUN pip freeze > requirements.txt

EXPOSE 5000

CMD ["bash"]