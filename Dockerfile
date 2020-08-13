FROM nikolaik/python-nodejs:python3.6-nodejs14

COPY Pipfile /Pipfile
COPY Pipfile.lock /Pipfile.lock
COPY package.json /package.json
COPY yarn.lock /yarn.lock

RUN apt-get update && apt-get install -y unzip

#install google-chrome, rsvg-convert, vim
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable
RUN apt-get install -y vim

#install ChromeDriver
ADD https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

# install Noto sans CJK jp
RUN cd /tmp && \
    mkdir noto && \
    curl -O -L https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip && \
    unzip NotoSansCJKjp-hinted.zip -d ./noto && \
    mkdir -p /usr/share/fonts/noto && \
    cp ./noto/*.otf /usr/share/fonts/noto/ && \
    chmod 644 /usr/share/fonts/noto/*.otf && \
    fc-cache -fv && \
    rm -rf NotoSansCJKjp-hinted.zip ./noto

RUN yarn install
RUN pip3 install pipenv
RUN pipenv install --system --deploy

CMD ["python3", "src/main.py"]
