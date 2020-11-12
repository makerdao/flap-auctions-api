FROM python:3.6.6

RUN groupadd -r maker && useradd --no-log-init -r -g maker maker

WORKDIR /home/maker/flap-auctions-ui

COPY bin bin
COPY lib lib
COPY flap_auctions flap_auctions
COPY install.sh install.sh
COPY requirements.txt requirements.txt

RUN pip3 install virtualenv && \
  ./install.sh && \
  chown -R maker:maker /home/maker

USER maker

ENTRYPOINT ["bin/flap-auctions"]