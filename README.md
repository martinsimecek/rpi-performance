# RPi Performance
Raspberry Performance Tracker

## Basic info
- Owner: Martin Simecek
- Contact: hello@martinsimecek.cz

## About
This app consists of a single Python file **performance.py** and MariaDB database (single data table). All measured indicators are taken from GPIO interface - [Gpiozero](https://gpiozero.readthedocs.io/en/stable/). Data is saved to **rpi.performance** table. The communication between Python and MariaDB is maintained with [MariaDB Connector/Python](https://mariadb.com/docs/appdev/connector-python/). Measurements can be also displayed in CLI in real time.

## Setup

### Clone repository
    cd /home/pi/Documents
    git clone https://github.com/martinsimecek/rpi-performance

### Install libraries
    sudo apt install mariadb-server
    sudo mysql_secure_installation
    pip3 install mariadb

### MariaDB database
Log in to MariaDB as **root** user and run following SQL commands. Note that you have to change **password** of user to be granted to INSERT (same password has to be set in the script).

    CREATE DATABASE rpi;
    CREATE USER 'collector'@'localhost' IDENTIFIED BY '<password>';
    GRANT INSERT ON rpi.* TO 'collector'@'localhost';
    FLUSH PRIVILEGES;
    USE rpi;
    CREATE TABLE performance (
      id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
      created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
      created_by VARCHAR(255) NOT NULL DEFAULT USER(),
      measured_on DATETIME NULL,
      cpu_temperature DECIMAL(4,2) NULL,
      disk_usage DECIMAL(4,2) NULL,
      load_average1 DECIMAL(4,2) NULL,
      load_average5 DECIMAL(4,2) NULL,
      load_average15 DECIMAL(4,2) NULL,
      server_host VARCHAR(255) NULL,
      server_response TINYINT(1) NULL,
      PRIMARY KEY (id)
    );
    EXIT

### Edit rc.local
If you want this script to be started automatically, paste the following code (before exit statement) into the `/etc/rc.local` file.

    # Run performance.py
    cd /home/pi/Documents/rpi-performance
    su pi -c "python3 performance.py" &
