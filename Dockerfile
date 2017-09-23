FROM debian:jessie AS fonts

RUN apt-get update
RUN apt-get install -y wget unzip
RUN wget -q https://ja.osdn.net/downloads/users/8/8642/genjyuugothic-20150607.zip
RUN unzip -q genjyuugothic-20150607.zip


FROM python:3.6
MAINTAINER lightnet328<lightnet328@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y nodejs npm
RUN npm cache clean && npm install n -g
RUN n stable && ln -sf /usr/local/bin/node /usr/bin/node
RUN apt-get purge -y nodejs npm

RUN apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 sudo git make curl xz-utils file

WORKDIR /root
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y

ADD . /var/www
WORKDIR /var/www
RUN mkdir /fonts
COPY --from=fonts /GenJyuuGothic-Light.ttf /fonts
RUN pip install -r requirements.txt
RUN npm install && npm run build
