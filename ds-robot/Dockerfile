FROM python:3.9
LABEL maintainer="ifui <ifui@foxmail.com>"

COPY ./scrapy.cfg /root/ds-robot/scrapy.cfg
COPY ./requirements.txt /root/ds-robot/requirements.txt

WORKDIR /root/ds-robot
ARG PYPI_MIRROR
RUN pip install -i ${PYPI_MIRROR} -r requirements.txt --trusted-host=${PYPI_MIRROR}

CMD ["scrapyd"]
