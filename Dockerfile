ARG username
ARG password
FROM debian:bullseye
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -yq install  wget vim systemctl apache2 sudo cron mosquitto mosquitto-clients  apt-utils dialog
RUN apt-get update
RUN apt-get install -y libapache2-mod-php7.4  sqlite3
RUN apt-get update
COPY ./setup_script setup_script
RUN chmod +x ./setup_script
RUN ./setup_script --thermiq_mqtt --mosquitto # 2>&1 | tee /var/thermiq_install.log
RUN mosquitto_passwd -b -c /etc/mosquitto/passwd "$username" "$password"
COPY ./mosquitto/mosquitto.conf /etc/mosquitto

#4J52JTPRC7AP5626
#docker run  \
#	-v /home/ostlund/thermia/pv/sqlite:/var/sqlite \
#	-v  /home/ostlund/thermia/pv/opt/etc:/opt/etc  \
#	-v  /home/ostlund/thermia/pv/www:/var/www \
#	-v /tmp/scratch:/tmp/scratch \
#	-p 8888:80 \
#	-p 9883:1883 --rm -it thermiq /bin/bash
## /etc/init.d/apache2 start

