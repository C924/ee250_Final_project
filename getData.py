import re
import subprocess
from influxdb import InfluxDBClient

# this calls the speedtest CLI (this is what i'm using to monitor the network speed)
response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

# storing the data from the Speedtest CLI software that can be written to a python dictionary
ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
jitter = jitter.group(1)

# python dictionary to store data from my RPi
# this data is then read from any IoT device to see what my internet speed is over say 12 hours.
speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "RaspberryPiCarlC"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping),
            "jitter": float(jitter)
        }
    }
]
# instantiates the influxDBClient and connects to my InfluxDB database named "internetspeed"
# this is where the data is stored from the python dictionary
client = InfluxDBClient('localhost', 8086, 'CarlC', 'ee250', 'internetspeed')

# this writes to my influxDB server and this is what allows me to use the data on grafana
client.write_points(speed_data)