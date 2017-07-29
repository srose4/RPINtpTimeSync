#!/usr/bin/env python

# This scipt was written for the Raspberry Pi to solve a boot up issue of time being stale
# since the gateway takes a very long time to connect over 3G
# Run this script with CRON to keep checking time, put in root's crontab
# */5 * * * * python /home/pi/timecheck.py >> /var/log/syslog 2>&1

import logging
import ntplib
import os
from time import ctime, time

STALEDELTA = (5 * 60)  # 5 minutes
NTP_EXE = '/etc/init.d/ntp'
NTP_RESTART = '/etc/init.d/ntp restart'
NTP_SERVER = 'pool.ntp.org'


def check_time():
    logging.debug('Executing check_time')
    # Open a NTP client
    ntp = ntplib.NTPClient()
    try:
        # Query NTP for time
        response = ntp.request(NTP_SERVER)
    except Exception:
        # If unable to get internet time
        logging.debug('Error getting internet time')
        return
    # Able to get internet time
    ntp_time = response.tx_time
    # Get the system time
    systime = time()
    # Debugging
    logging.debug('Internet: {0}'.format(ctime(response.tx_time)))
    logging.debug('System: {0}'.format(ctime(systime)))
    # If system time is stale
    if (ntp_time - systime) >= STALEDELTA:
        # Does the Raspberry Pi NTP script exists
        if os.path.exists(NTP_EXE):
            # Restart the NTP service
            os.system(NTP_RESTART)
            logging.warning('Time is stale - Restarting NTP')
    else:
        # Time is not stale
        logging.debug('Time is within delta')
        return

if __name__ == "__main__":
    # Change for debugging
    logging.basicConfig(level=logging.WARNING)
    check_time()
