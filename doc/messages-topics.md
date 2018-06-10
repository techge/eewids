Topic Exchange Setting for "messages"
=====================================

This page tracks all information for topic exchange 'messages', where every application reports things happening around.

*Note*: This information is still in constant change and not considered stable yet.

## Routing Keys

An application can create a RabbitMQ queue and bind it to the 'messages' exchange by using various routing keys. Every application can publish or subscribe to information like warnings, errors etc. on the message broker by using the following routing key scheme:

    <service>.<loglevel>

'service' is the name of the application which publishs a message, e.g. 'kismet-server', 'kismet2rabbit' or alike. 'loglevel' is one of the follwing: 

* info
* warning
* error
* alert
* critical
