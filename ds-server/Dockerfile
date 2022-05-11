FROM python:3.9
LABEL maintainer="ifui <ifui@foxmail.com>"

COPY ./requirements.txt /root/ds-server/requirements.txt

# install packages
WORKDIR /root/ds-server
ARG PYPI_MIRROR
RUN pip install -i ${PYPI_MIRROR} -r requirements.txt --trusted-host=${PYPI_MIRROR}

CMD [ "sh","/root/ds-server/scripts/run.sh" ]
