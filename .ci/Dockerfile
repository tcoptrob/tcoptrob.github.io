FROM --platform=x86_64 ubuntu:22.04

ARG USERNAME="tcoptrob"
ARG HOME_DIR="/home/${USERNAME}"

ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Europe/Athens"

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-pip git && apt-get clean

RUN pip3 install pymdown-extensions==9.9.2 && pip3 cache purge
RUN pip3 install py-markdown-table==0.3.3 && pip3 cache purge
RUN pip3 install mkdocs==1.4.2 && pip3 cache purge
RUN pip3 install mkdocs-material==9.0.9 && pip3 cache purge
RUN pip3 install mkdocs-pymdownx-material-extras==2.4.2 && pip3 cache purge
RUN pip3 install mkdocs-blogging-plugin==2.2.2 && pip3 cache purge

# User stuff
RUN useradd -ms /bin/bash $USERNAME
RUN echo "${USERNAME}:pass" | chpasswd
RUN apt install -y sudo
RUN usermod -aG sudo $USERNAME

USER $USERNAME

# Working directory
WORKDIR ${HOME_DIR}
