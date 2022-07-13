FROM debian:bullseye

RUN apt-get update \
        && apt-get install python3 python3-pip -y \
        && useradd -m -d /home/yayo-oldman yayo-oldman \
        && usermod --shell /bin/bash yayo-oldman \
        && pip3 install cryptography

## For testing purposes ##
ENV bobspwd 1234
RUN useradd --no-create-home bob \
        && echo "bob:${bobspwd}" | chpasswd
##          **          ## 

COPY ./calculadora /tmp/calculadora/

COPY --chown=yayo-oldman:yayo-oldman ./infection /home/yayo-oldman/infection/

USER yayo-oldman

WORKDIR /tmp/calculadora

CMD /bin/bash
