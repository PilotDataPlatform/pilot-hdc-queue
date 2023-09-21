# Queue Service

## About
Queue service contains three sub-services. Each of them is responsible for different functions. It consists of different components to run and monitor pipelines.

## Queue Consumer
This component developed to connect with RabbitMQ and consume received  messages


## Queue Producer
It is a mini flask application connected with RabbitMQ, developed to send message to queue

## Queue Socketio
This component enables low-latency, bidirectional and event-based communication between a client and a server.

## Acknowledgements
The development of the HealthDataCloud open source software was supported by the EBRAINS research infrastructure, funded from the European Union's Horizon 2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3) and H2020 Research and Innovation Action Grant Interactive Computing E-Infrastructure for the Human Brain Project ICEI 800858.
