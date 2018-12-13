FROM alpine
ADD ./application/ /application
COPY requirements.txt /tmp
COPY entrypoint.sh /entrypoint.sh
RUN /sbin/apk update && \
      /sbin/apk add python3 && \
      /sbin/apk add --no-cache --virtual build-deps build-base python3-dev linux-headers && \
      /usr/bin/pip3 install -r /tmp/requirements.txt && \
      /sbin/apk del build-deps && \
      /bin/rm -rf /var/cache/apk/*
EXPOSE 8080
STOPSIGNAL SIGINT
ENTRYPOINT /entrypoint.sh
