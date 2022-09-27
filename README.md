# thermiq-docker

## Install

###  Before beginning have on hand 
  - Your Order Email
  - Your 16 digit license key XXXXXXX
  - Choose a USERNAME to be used as MQTTTServer_User
  - Choose a PASSWORD to be used as MQTTServer_PW 
  - Find your  MQTTClient_Name = ThermIQ_XXXXXXXXX 

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

The configured image will be created by creating a new image from the running container.

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

