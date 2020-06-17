FROM ubuntu:18.04

COPY src /src
COPY config /config

COPY Pipfile /Pipfile
COPY Pipfile.lock /Pipfile.lock
COPY package.json /package.json
COPY yarn.lock /yarn.lock

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt update -y && apt upgrade -y
RUN apt install -y chromium-browser
RUN apt install -y chromium-chromedriver
RUN apt install -y curl
RUN apt-get install -y git
RUN apt install -y python3.6
RUN apt install -y python3-pip

RUN apt install -y nodejs npm

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y && apt-get install -y yarn

RUN npm install -g n
RUN n latest
RUN apt purge -y nodejs npm

RUN yarn install
RUN pip3 install pipenv
RUN pipenv install --system --deploy

CMD ["python3", "src/main.py"]
