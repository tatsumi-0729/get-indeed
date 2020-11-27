FROM python:3
USER root

WORKDIR /app

COPY /app /app

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# Japanese Localization
RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get install -y vim less
RUN pip install --upgrade pip && \
pip install --upgrade setuptools && \
pip install selenium && \
pip install matplotlib

# google-chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# ChromeDriver
ADD https://chromedriver.storage.googleapis.com/75.0.3770.8/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

CMD ["python","main.py"]