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

