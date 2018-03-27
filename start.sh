#!/bin/sh

#echo "switch of WiFi"
#sudo ifconfig wlp2s0 down
#sudo iwconfig wlp2s0 mode managed 
#sudo ifconfig wlp2s0 up

echo "Starting RabbitMQ"
docker run -tid --net=host rabbitmq

echo "Starting Kismet Stuff"
docker run -tid --net=host eewids/kismet
sleep 7
/usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=wlp2s0 &

sleep 3
echo "Starting Rabbit-recv"
docker run -ti --net=host rabbit-recv

echo "killing everything :)"
docker stop $(docker ps -q)
kill %%

echo "Ich warte einfach mal"
#sleep 5

#echo "Try to restore WiFi"
#sudo ifconfig wlp2s0 down
#sudo iwconfig wlp2s0 mode managed
#sudo ifconfig wlp2s0 up
