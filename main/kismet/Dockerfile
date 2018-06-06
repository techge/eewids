FROM debian:stretch-slim as builder

# Install necessary packages for building
RUN apt-get update && apt-get install -y \
    autoconf \
    build-essential \
    git \
    gdb \
    gdbserver \
    libcap-dev \
    libdw-dev \
    libfftw3-3 \
    libmicrohttpd-dev \
    libncurses5-dev \
    libnl-3-dev \
    libnl-genl-3-dev \
    libnm-dev \
    libpcap-dev \
    librtlsdr0 \
    libsqlite3-dev \
    libmicrohttpd-dev \
    libprotobuf-dev \
    libprotobuf-c-dev \
    pkg-config \
    protobuf-compiler \
    protobuf-c-compiler \
    #python \
    #python-setuptools \
    #python-protobuf \
    #python-sqlite \
    #python-requests \
    unzip \
    zlib1g-dev

# Clone git repo and build kismet
RUN git clone https://github.com/kismetwireless/kismet.git /opt/kismet && \
    cd /opt/kismet && \
    ./configure --disable-python-tools && \
    make && \
    make install

########################################################################
# Start from official Debian Stretch-slim image 
FROM debian:stretch-slim

# Install dependencies of kismet 
RUN apt-get update && apt-get install -y \
    libbz2-1.0 \
    libc6 \
    libcap2 \
    libdw1 \
    libelf1 \
    libffi6 \
    libgcc1 \
    libgcrypt20 \
    libglib2.0-0 \
    libgnutls30 \
    libgmp10 \
    libgomp1 \
    libgpg-error0 \
    libhogweed4 \
    libidn11 \
    libmicrohttpd12 \
    libncurses5 \
    libnettle6 \
    libnl-3-200 \
    libnl-genl-3-200 \
    libnm0 \
    libp11-kit0 \
    libpcap0.8 \
    libpcre3 \
    libprotobuf10 \
    libprotobuf-c1 \
    libsqlite3-0 \
    libstdc++6 \
    libtasn1-6 \
    libtinfo5 \
    liblzma5 \
    zlib1g \
    && rm -rf /var/lib/apt/lists/* && \
    apt-get clean -y && apt-get autoclean -y

COPY --from=builder /usr/local/ /usr/local/

# Create user 'kismet' and add to new group kismet
RUN groupadd -r kismet && useradd -m -g kismet kismet 

# Make capture binaries setuid, so that user kismet can start them
RUN chmod u=rsx,g=rx,o-rwx /usr/local/bin/kismet_cap_linux_wifi && \
    chown :kismet /usr/local/bin/kismet_cap_linux_wifi && \
    chmod u=rsx,g=rx,o-rwx /usr/local/bin/kismet_cap_linux_bluetooth && \
    chown :kismet /usr/local/bin/kismet_cap_linux_bluetooth

ADD kismet.conf /usr/local/etc/
ADD kismet_httpd.conf /home/kismet/.kismet/
ADD kismet_httpd.conf /root/.kismet/

# TODO Start as Kismet user, instead of root
#USER kismet

CMD ["/usr/local/bin/kismet", "--no-ncurses"]

EXPOSE 2501
EXPOSE 3501
