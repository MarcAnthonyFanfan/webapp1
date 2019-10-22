FROM ubuntu:19.10

RUN apt update && \
    apt upgrade -y

RUN apt install -y git python3-pip

RUN pip3 install flask

RUN git clone https://github.com/MarcAnthonyFanfan/webapp1

EXPOSE 5000

CMD ["bash"]