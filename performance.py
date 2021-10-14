# Import modules
import time
import mariadb
from sys import exit
from gpiozero import CPUTemperature, DiskUsage, LoadAverage, PingServer

# Configurate database connection
config = {
   'user': 'collector',
   'password': '<password>',
   'host': 'localhost',
}

# Connect to database
try:
  conn = mariadb.connect(**config, database='rpi')
except mariadb.Error as e:
  print(f"Error connectiong to MariaDB Platform: {e}")
  exit(1)

# Prepare database
cur = conn.cursor()
conn.autocommit = True

# Infinite loop
while True:

    # Prepare data
    measured_on = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    cpu_temperature = round(CPUTemperature().temperature,2)
    disk_usage = round(DiskUsage().usage,2)
    load_average1 = LoadAverage(minutes=1).load_average
    load_average5 = LoadAverage(minutes=5).load_average
    load_average15 = LoadAverage(minutes=15).load_average
    server_host = 'seznam.cz'
    server_response = PingServer(server_host).value

    # Insert data to MariaDB
    cur.execute("INSERT INTO rpi.performance (measured_on, cpu_temperature, disk_usage, load_average1, load_average5, load_average15, server_host, server_response) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (measured_on, cpu_temperature, disk_usage, load_average1, load_average5, load_average15, server_host, server_response))

    # Print data (disabled)
    # print('\n\nMeasured on:', measured_on, '\nCPU Temperature:', cpu_temperature, '°C\nDisk usage:', disk_usage, '%\nLoad average:', load_average1, '(1 min),', load_average5, '(5 min),', load_average15, '(15 min)\nServer response:', server_response, '-', server_host)

    # Pause for 1 minute
    time.sleep(60)
