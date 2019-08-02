FROM django:python2

RUN apt-get update && apt-get install -y \
  build-essential \
  libldap2-dev \
  libsasl2-dev \
  libffi-dev \
&& apt-get clean  \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./entrypoint.sh /
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
