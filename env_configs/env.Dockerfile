FROM debian:buster-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    g++ \
    git \
    libbz2-dev \
    libffi-dev \
    libjpeg-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    llvm \
    make \
    python3-dev \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev

RUN curl https://pyenv.run | bash

ENV PATH="/root/.pyenv/bin:/root/.pyenv/shims:/root/.pyenv/versions/3.7.12/bin:$PATH"
RUN echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

RUN /root/.pyenv/bin/pyenv install 3.7.12
RUN /root/.pyenv/bin/pyenv install 3.8.12
RUN /root/.pyenv/bin/pyenv install 3.9.7
RUN /root/.pyenv/bin/pyenv install 3.10.2
RUN /root/.pyenv/bin/pyenv install 3.11.0
RUN /root/.pyenv/bin/pyenv install 3.12.0
RUN /root/.pyenv/bin/pyenv install 3.13.0
RUN /root/.pyenv/bin/pyenv install 3.14-dev

RUN /root/.pyenv/bin/pyenv global 3.7.12 3.8.12 3.9.7 3.10.2 3.11.0 3.12.0 3.13.0 3.14-dev

COPY pyproject.toml /app

RUN python -m pip install .[dev] && python -m pip install tox

COPY .. /app
