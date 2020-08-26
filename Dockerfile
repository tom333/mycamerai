# Dockerfile for providing buildozer
#
# Build with:
# docker build --tag=kivy/buildozer .
#
# In order to give the container access to your current working directory
# it must be mounted using the --volume option.
# Run with (e.g. `buildozer --version`):
# docker run \
#   --volume "$HOME/.buildozer":/home/user/.buildozer \
#   --volume "$PWD":/home/user/hostcwd \
#   kivy/buildozer --version
#
# Or for interactive shell:
# docker run --interactive --tty --rm \
#   --volume "$HOME/.buildozer":/home/user/.buildozer \
#   --volume "$PWD":/home/user/hostcwd \
#   --entrypoint /bin/bash \
#   kivy/buildozer
#
# If you get a `PermissionError` on `/home/user/.buildozer/cache`,
# try updating the permissions from the host with:
# sudo chown $USER -R ~/.buildozer
# Or simply recreate the directory from the host with:
# rm -rf ~/.buildozer && mkdir ~/.buildozer

FROM python:3.8-slim


ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/hostcwd" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

ENV http_proxy="http://proxy-web.proxy-dmz.gnc:3128"
ENV https_proxy="http://proxy-web.proxy-dmz.gnc:3128"
ENV ftp_proxy="http://proxy-web.proxy-dmz.gnc:3128"
ENV no_proxy="localhost,127.0.0.1,127.0.1.1,gitlab-infra.ref.gnc,.recif.nc,.appli-gestion.nc,.gnc,/var/run/docker.sock,10.10.106.0/24,.valid-gouv.nc,.dmz.nc,jira.gouv.nc,jira-info.gouv.nc,webnotes.gouv.nc,stats-new.gouv.nc,guichet-entreprises.nc,192.168.62.38"

ENV HTTP_PROXY="http://proxy-web.proxy-dmz.gnc:3128"
ENV HTTPS_PROXY="http://proxy-web.proxy-dmz.gnc:3128"
ENV FTP_PROXY="http://proxy-web.proxy-dmz.gnc:3128"
ENV NO_PROXy="localhost,127.0.0.1,127.0.1.1,gitlab-infra.ref.gnc,.recif.nc,.appli-gestion.nc,.gnc,/var/run/docker.sock,10.10.106.0/24,.valid-gouv.nc,.dmz.nc,jira.gouv.nc,jira-info.gouv.nc,webnotes.gouv.nc,stats-new.gouv.nc,guichet-entreprises.nc,192.168.62.38"


RUN echo "Acquire::http::Proxy \"http://proxy-web.proxy-dmz.gnc:3128\";" > /etc/apt/apt.conf.d/proxy
RUN echo "Acquire::https::Proxy \"http://proxy-web.proxy-dmz.gnc:3128\";" >> /etc/apt/apt.conf.d/proxy

RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="fr_FR.UTF-8" \
    LANGUAGE="fr_FR.UTF-8" \
    LC_ALL="fr_FR.UTF-8"

# bug cf https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=863199#23
RUN mkdir -p /usr/share/man/man1

RUN DEBIAN_FRONTEND=noninteractive  apt install wget gnupg software-properties-common --yes --no-install-recommends

RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add -

RUN add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/

# system requirements to build most of the recipes
RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    autoconf \
    automake \
    build-essential \
    ccache \
    cmake \
    gettext \
    git \
    libffi-dev \
    libltdl-dev \
    libssl-dev \
    libtool \
    adoptopenjdk-8-hotspot \
    patch \
    pkg-config \
    python3-all-dev \
    sudo \
    unzip \
    zip \
    zlib1g-dev

# prepares non root env
RUN useradd --create-home --shell /bin/bash ${USER}
# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}
WORKDIR ${WORK_DIR}

# installs buildozer and dependencies
RUN pip3 install --user --upgrade Cython wheel pip virtualenv buildozer #==0.29.19

ENTRYPOINT ["buildozer"]