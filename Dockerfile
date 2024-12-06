FROM python:3.12

ENV APP /ppocr

RUN mkdir $APP
WORKDIR $APP

COPY requirements.txt api.py ./

RUN sed -i 's#deb.debian.org/debian$#mirrors.tuna.tsinghua.edu.cn/debian#' /etc/apt/sources.list.d/debian.sources \
        && apt clean \
        && apt update -y \
        && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
        && pip install --upgrade pip \
        && pip install -r requirements.txt \
        && apt-get install ffmpeg libsm6 libxext6  -y \
        && apt-get clean 

EXPOSE 5000
CMD ["/bin/bash","-c","python3 ./api.py"]