FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /crawl

# COPY ./crawl .

# RUN pip install -r requirements.txt

# ENTRYPOINT [ "python", "go-spider.py" ]

RUN mkdir -p /scrapyrt/src /scrapyrt/project
RUN mkdir -p /var/log/scrapyrt

ADD ./scrapyrt /scrapyrt/src
RUN pip install /scrapyrt/src scrapy-splash

COPY ./crawl /scrapyrt/project

WORKDIR /scrapyrt/project

ENTRYPOINT ["scrapyrt", "-i", "0.0.0.0"]

EXPOSE 9080

