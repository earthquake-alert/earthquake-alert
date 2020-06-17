FROM nikolaik/python-nodejs:python3.6-nodejs14

COPY src /src

COPY Pipfile /Pipfile
COPY Pipfile.lock /Pipfile.lock
COPY package.json /package.json
COPY yarn.lock /yarn.lock

RUN apt-get update
RUN apt-get install -y librsvg2-bin
RUN apt-get install -y vim


RUN yarn install
RUN pip3 install pipenv
RUN pipenv install --system --deploy

CMD ["python3", "src/main.py"]
