# Monitoring App for LF8
The goal of this project is to log your system information and trigger an email to warn
you if your system information is equal or higher than your thresholds.

There is a webserver where you can see the history of the logs.

# Requirements
- Docker
- SMTP server
- Python 3.11 (only if you won't use docker)

# Setup
## testing

- on first setup use creation sql file from 
[```monitoring-app-database```](https://github.com/itech-lf-team-pina/monitoring-app-database) 
to create database with tables on your database server or in your local test database in docker

- there is a ```config.ini.dist``` which you can copy and rename in ``config.ini``
- in root folder use ```docker compose up``` to start local database and monitoring app

# Authors
This project is brought to you by Adrian, Nils, Ibrahim and Pascal.
