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
    unzip \
    zlib1g-dev

# Clone git repo and build kismet
RUN git clone https://github.com/kismetwireless/kismet.git /opt/kismet && \
    cd /opt/kismet && \
    ./configure --disable-python-tools && \
    make -j4 && \
    make install

# This is kismet server only, no need for capture-tools
RUN rm /usr/local/bin/kismet_cap*

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
    libp11-kit0 \
    libpcap0.8 \
    libpcre3 \
    libprotobuf10 \
    libsqlite3-0 \
    libstdc++6 \
    libtasn1-6 \
    libtinfo5 \
    liblzma5 \
    zlib1g \
    && rm -rf /var/lib/apt/lists/* && \
    apt-get clean -y && apt-get autoclean -y

COPY --from=builder /usr/local/ /usr/local/


# Start Kismet with user privileges
RUN useradd -m kismet 
USER kismet 

# Add config files
ADD kismet.conf /usr/local/etc/
ADD kismet_httpd.conf /home/kismet/.kismet/

CMD ["/usr/local/bin/kismet", "--no-ncurses"]

EXPOSE 2501
EXPOSE 3501
