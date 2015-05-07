FROM ubuntu:14.04

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -q -y openssl

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/bin
WORKDIR /root

ADD bin /root/bin
ADD common /root/common

CMD ["usage"]
