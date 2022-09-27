# thermiq-docker

Since I had a perfectly good Intel NUC at home, I did not want to invest in additional hardware and buy a Raspberry PI. This describes installing [Thermiq-MQTT](https://thermiq.net) using docker running on my Intel NUC.  It finally worked just fine. Here is my documentation of the process. 

Some things to note:

- The container is running apache on port 80 and MQTT on port 1883 **inside the container**
- The ports 80 and 1883 in the container is mapped to 8888 and 9883 on localhost to not conflict with other services on localhost
	- Since ports 8888 and 9883 are used the mapped ports rather than the traditional ports are used when accessing services inside the container. 
	- In particular, seeing output from ThermIQ in MQTT Explorer (below) will  use 9883 instead of 1883
	- The poller and card will be seen outside the container  on port 8888 instead of port 80 
	
## Docker Install

###  Before beginning have on hand 
  - Your Order Email
  - Your 16 digit license key XXXXXXX
  - Choose a USERNAME to be used as MQTTTServer_User
  - Choose a PASSWORD to be used as MQTTServer_PW 
 

### Get started and build the docker base image

``` 
export USERNAME=uuuuu
export PASSWORD=pppppp
docker build --build-arg password=${PASSWORD} --build-arg username=${USERNAME} -t thermiq-docker .
```
### Now configure the server

```
docker-compose -f docker-compose-configure.yaml up 
```
Now open up http://localhost:8888 

- Initial Config  sqlite  should be selected 
-  Press  **Download ThermIQ**
	- insert Order Email and click  checkmark
	-  insert Licence key  and click checkmark
 
- press **Download**  and install released version (twice!)
- press Press **User Database** -> Update User datbase
	- If necessary chmod a+w on pv/sqlite and pv/sqlite/*
- press **Main Database** -> Create and init main Database or Update if it exists
- skip Dropbox   
- press **Secure installation** 
	- insert USERNAME and click check
	- insert PASSWORD  and click check
	- Remove password protection
- Press **Start**

### Configure the ThermIQ_MQTT card

- follow the instructions from thermiq.net until you get the card working on your local network. 

### Configure MQTT_Explorer [MQTT Explorer](https://mqtt-explorer.com/) 

Thanks Thomas Nordquist!

You should definitely get MQTT_Explorer working with your card. It is less fragile than ThermIQ


- MQTT Connection paramters
	- Protocoll mqtt://
	- Host: localhost or IP
	- Port: 9883 **This is not a mistake**  MQTT is listening to 1883 inside the container which is mapped to 9883 on localhost
	- Username and password according to USERNAME and PASSWORD
	- Save
	- Connect
- After a minute, ThermIQ should have a message; 
	- Note the MQTT_NODE probably **ThermIQ-mqtt-bb** 
	- Open the drobdown and note the Client_name  which is needed in the next step
- If nothing is working try test 
	- test.mosquitto.org
	- protocoll mqtt://
	- host: test.mosquitto.org
	- port: 1833 **Yes 1883 here since this is not addressing the container**
	- username: wildcard
	- password: leave blank
	- press Save
	- press Connect
	- a bunch of messages should appear.
- If you receiving  register data you are in good shape and your card is communicating with MQTT_Server
- If you cannot get any message from ThermIQ your card is not communicating with MQTT and you must fix that.
	- Weak wifi?
	- Misconfigured card? Follow instructions for installing your card in your wifi network
- If you are getting a message from ThermQI  in MQTT Explorer  but no register data,  perhaps your card is not plugged in to the heatpump.
- If your card is not plugged in to the heatpump you can continue to the next steps but you won't see any register data at all and you won't be able to tell if the database is being accessed properly. 

### Configure poller

got to http://localhost:8888

- login and go to settings -> poller settings
- put in 
	- MQTTServer_IP = 0.0.0.0 
	- MQTTServer_Port - 1883
	- MQTTServer_User = USERNAME
	- MQTTServer_PW = PASSWORD
	- MQTTServer_Cafile = Empty
	- MQTTClient_Name = Get from MQTT Explorer ThermIQ_30AEA46ABBB8
	- MQTTNode  = ThermIQ/ThermIQ-mqtt-bb  **Note this is prefilled out incorrectly the last -bb is missing**
	- Action -> Enable both boxes

### Now configure server poller

```
docker  exec -it thermiq-docker_thermiq_1 /bin/bash
sudo systemctl restart ThermIQ*_listener*
sudo systemctl restart mosquitto

```
Leave this docker shell running; be prepared to restart the services when making changes

### Check that things are working

Got to http://localhost:8888 and login  

**The following caused the most headaches; getting ThermIQ communicating with MQTT Server**

- check that Thermia -> Overview registers are populated. if not
	- Make sure your card is working with MQTTExplorer. Get that working before coming back here
	- Read off the ClientName from the MQTTExplorer messages
	- Check over MQTTNode in the ThermIQ ;   **it ends with -bb ; don't accept the default** ; go back to Update and Install to fix
	- Check permissions on sqlite , it should be writable and owned by www-data:www-data
- check that you can write to register for instance Indoor target temp
	- If you appear to be able to write to the register but the register is not saved on refresh
		- check over the MQTTNode in poller settings; don't forget to restart listeners in the docker shell
		- check permissions  of sqlite database sudo chown -R www-data:www-data /var/sqlite
		- perhaps chmod a+w on these
		- check these permission on host and image

#### Create  the active image

Once you have the docker image working, a preconfigured image will be created by cloing  a new image from the running container.

```
docker ps # read off CONTAINER_ID ; mine was  4c0bc1b30bc4
docker commit  4c0bc1b30bc4 thermiq-docker:configured
```

- now control-C out of running container
    -  if permission error, run script stop-container

```
docker-compose up -d
```

- Check  localhost:8888 

