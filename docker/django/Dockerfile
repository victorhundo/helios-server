FROM python:2.7

RUN apt-get update && apt-get install -y \
  build-essential \
  libldap2-dev \
  libsasl2-dev \
  libffi-dev \
  curl \
  postgresql \
&& apt-get clean  \
&& rm -rf /var/lib/apt/lists/*

ENV TZ=America/Recife
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY ./entrypoint.sh /
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
