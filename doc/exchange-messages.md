Fields of Messages Submitted to Exchange "messages"
===================================================

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

## Fields Available for Captured Data

Key | Description of field | since version
----| -------------------- | -------------
version | Indicates the availability of fields as noted on this page | 1.0
name | Alert name | 1.0
text | Alert text | 1.0
loglevel | This is either 'info', 'warning', 'error', 'alert' or 'critical' | 1.0

It is possible to define further fields, as alerts are just json-formatted information. Every App can add and define own fields, but must have at least the above ones. Self definied fields should be stable and documented though.
