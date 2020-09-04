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
#RUN useradd --create-home --shell /bin/bash ${USER}
## with sudo access and no password
#RUN usermod -append --groups sudo ${USER}
#RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
#
#USER ${USER}


# installs buildozer and dependencies
RUN pip3 install --user --upgrade Cython==0.29.19 wheel pip virtualenv buildozer toml colorama jinja2 python-for-android
ENV PATH="/root/.local/bin:$PATH"

#Install du NDK
ENV ANDROID_NDK_HOME /opt/android-ndk
ENV ANDROID_NDK_VERSION r19c

RUN mkdir /opt/android-ndk-tmp && \
    cd /opt/android-ndk-tmp && \
    wget -q https://dl.google.com/android/repository/android-ndk-${ANDROID_NDK_VERSION}-linux-x86_64.zip && \
# uncompress
    unzip -q android-ndk-${ANDROID_NDK_VERSION}-linux-x86_64.zip && \
# move to its final location
    mv ./android-ndk-${ANDROID_NDK_VERSION} ${ANDROID_NDK_HOME} && \
# remove temp dir
    cd ${ANDROID_NDK_HOME} && \
    rm -rf /opt/android-ndk-tmp

# add to PATH
ENV PATH ${PATH}:${ANDROID_NDK_HOME}

#Install du sdk
ARG ANDROID_SDK_VERSION=6514223
ENV ANDROID_SDK_ROOT /opt/android-sdk
RUN mkdir -p ${ANDROID_SDK_ROOT} && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip && \
    unzip *tools*linux*.zip -d ${ANDROID_SDK_ROOT} && \
    rm *tools*linux*.zip

WORKDIR ${ANDROID_SDK_ROOT}
RUN yes 2>/dev/null | /opt/android-sdk/tools/bin/sdkmanager --sdk_root=/opt/android-sdk --licenses
RUN /opt/android-sdk/tools/bin/sdkmanager --sdk_root=/opt/android-sdk "build-tools;30.0.2"
RUN /opt/android-sdk/tools/bin/sdkmanager --sdk_root=/opt/android-sdk "platforms;android-28"

#Install de apache ANT
ARG ANT_VERSION=1.9.4
WORKDIR /opt
RUN wget -q http://archive.apache.org/dist/ant/binaries/apache-ant-${ANT_VERSION}-bin.tar.gz && \
    tar xzf apache-ant-*.tar.gz && \
    rm xzf apache-ant-*.tar.gz

WORKDIR ${WORK_DIR}
ENTRYPOINT ["buildozer"]