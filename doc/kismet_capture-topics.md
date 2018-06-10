Topic Exchange Setting for "kismet_capture"
===========================================

This page tracks all information for topic exchange 'kismet_capture', which is used by Kismet2Rabbit to publish all information to the packets Kismet captured.

*Note*: This information is still in constant change and not considered stable yet.

## Routing Keys

An application can create a RabbitMQ queue and bind it to the 'kismet_capture' exchange by using various routing keys. Kismet2Rabbit is submitting all parsed packets captured by Kismet to the message broker by using the following routing key scheme:

    <interfaceID>.<frameType>.<frameSubtype>

The routing key for a Beacon frame captured by the interface with interfaceID '00000000' would read:

    00000000.Management.Beacon

Instead of binding a queue to every possible routing key, one is encouraged to use topics. This is done by using the asterisk symbol. Thus, to get all Beacon frames, one uses `*.*.Beacon`. To get all management frames of one specific interface, one subscribes to `interID.management.*` instead and so on.

More information on RabbitMQs exchange types (remember Eewids is using topic exchanges) can be found [here](https://www.cloudamqp.com/blog/2015-09-03-part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html).
