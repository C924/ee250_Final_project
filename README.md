# ee250_Final_project
Team Members: Carl Campos

This is what you need to run this project:
1. You need to install gnupg1, apt-transpor-https, dirmengr, and lsb-release on your RPi to run the Speedtest CLI software:

sudo apt install apt-transport-https gnupg1 dirmngr lsb-release

2. Need to add this repository or the Speedtest CLI wont work:

echo "deb [signed-by=/usr/share/keyrings/speedtestcli-archive-keyring.gpg] https://packagecloud.io/ookla/speedtest-cli/debian/ $(lsb_release -cs) main" | sudo tee  /etc/apt/sources.list.d/speedtest.list

3. Now install the speedtest package:

sudo apt install speedtest

4. Now, I believe you can run the script without making your own influxDB database. But if this doesn't work you can do the following:

curl https://repos.influxdata.com/influxdata-archive.key | gpg --dearmor | sudo tee /usr/share/keyrings/influxdb-archive-keyring.gpg >/dev/null

5. Need to add InfluxDB repository, I used this command on Raspberry Pi OS:

echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

6. Now start InfluxDB on the RPi:

sudo systemctl start influxdb

7. Then you can create a database with the following commands:

influx
CREATE DATABASE internetspeed
CREATE USER "CarlC" WITH PASSWORD 'ee250'
GRANT ALL ON "internetspeed" to "CarlC"
quit

8. Now we need to install Grafana on the IoT device we want the process the data on:

curl https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana-archive-keyrings.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/grafana-archive-keyrings.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

9. With Grafana installed, we can access it by typing:

localhost:3000

10. Login to Grafna by using:

username: admin
password: admin

You can then create your own password.

11. Before we process the data on Grafana, run the script one time manually so that some data can be sent to InfluxDB.
12. Now, on Grafna do the following:

Go to configuration > data sources
> add data source > InfluxDB
> Under URL put this: http://localhost:8086
> Scroll down to Database and enter internetspeed
> then put CarlC as user
> then put ee250 for the password
> now click save and test and you should see something pop up that says "found one measurement" indicating Grafana found the data that we want to measure.

13. Now we need to create a dashboard on Grafana.

> Go to Dashboard > Create new Dashboard > add a new panel
> you should see "Quary" under the graph that has no data
> make sure InfluxDB is selected as a data source > click on select measurement (you should see internet_speed here, if no results are shown, Grafana can't access the data from InfluxDB).
> click field(value) and type download, upload, ping, or jitter (these names must match exactly with the Python dictionary from the script)
> next to mean() click the + and click Aggregations > Distinct
> do this for upload, download, and ping (can add jitter as well if needed)

14. Add this point you should see some of the data collected from InfluxDB graphed. This should be everything needed to fully run the project.

OPTIONAL: You can use crontab to automate the script and it run for some set interval of time to make the data more useful. I ran mine every min for testing but something more useful would be every hour over 24 hours to see the change in speed more clearly.
