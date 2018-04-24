Fields of Messages Submitted to Exchange "messages"
===================================================

This page tracks all fields of information submitted to RabbitMQ on exchange ['message'](messages-topics.md).

*Note*: This information is still in constant change and not considered stable yet.

Key | Description of field | since version
----| -------------------- | -------------
version | Indicates the availability of fields as noted on this page | 1.0
name | Alert name | 1.0
text | Alert text | 1.0

It is possible to define further fields, as alerts are just json-formatted information. Every App can add and define own fields, but must have at least the above one. Self definied fields should be stable though.
