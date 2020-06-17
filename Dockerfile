FROM nikolaik/python-nodejs:python3.6-nodejs14

COPY src /src
COPY config /config

COPY Pipfile /Pipfile
COPY Pipfile.lock /Pipfile.lock
COPY package.json /package.json
COPY yarn.lock /yarn.lock

RUN apt-get update && apt-get install -y unzip

#install google-chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable
RUN apt-get install librsvg2-bin

#install ChromeDriver
ADD https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

RUN yarn install
RUN pip3 install pipenv
RUN pipenv install --system --deploy

CMD ["python3", "src/main.py"]
