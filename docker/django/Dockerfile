FROM django:1.8.7-python2

RUN apt-get update && apt-get install -y \
  build-essential \
  libldap2-dev \
  libsasl2-dev \
  libffi-dev \
  curl \
&& apt-get clean  \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./entrypoint.sh /
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
