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

This project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101058516. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or other granting authorities. Neither the European Union nor other granting authorities can be held responsible for them.

![EU HDC Acknowledgement](https://hdc.humanbrainproject.eu/img/HDC-EU-acknowledgement.png)
