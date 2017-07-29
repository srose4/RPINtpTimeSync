# RPiNTPtimesync

This is a simple Python script that attempts to query a NTP server and  
if the system time is less than some delta, restart the NTP service.  

I wrote this for use on a Raspberry Pi only.  I have not tested it with  
other platforms.  The RPI was a IoT device with very poor internet  
connection. As such, system time kept getting out of sync when ever  
the RPI rebooted, and this RPI does not have a RTC.  

Requires Ntplib library, install using Pip on the RPI  
`sudo pip install ntplib`  

I call the script using a root cronjob. Run the command  
`sudo crontab -e`  
and insert this text into the file  
`*/5 * * * * python /home/pi/timecheck.py >> /var/log/syslog 2>&1`  


