FROM debian:stretch-slim

RUN apt-get update && apt-get install -y \
	build-essential \
    libpcap-dev \
	librabbitmq-dev

# TODO make sure all necessary components are installed
# TODO have look if it would work with alpine!

COPY amqp-utils.c .
COPY amqp-utils.h .
COPY eewids-cap.c .

RUN gcc -lpcap -lrabbitmq -o eewids-cap -Wpedantic -ggdb eewids-cap.c amqp-utils.c

ENTRYPOINT [ "./eewids-cap" ]
