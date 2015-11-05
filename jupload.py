# File: jupload.py
# Author: Tyler Jordan
# Modified: 4/15/2015
# Purpose: Assist CBP engineers with Juniper configuration tasks

import os, sys, logging
import utility

from utility import *
from jnpr.junos import Device
from jnpr.junos.utils.sw import SW
from jnpr.junos.exception import *
from getpass import getpass

host = ''             
package = ''
remote_path = '/var/tmp'
validate = True
logfile = '.\\logs\\install.log'
code_path = '.\\junos\\'


def do_log(msg, level='info'):
    getattr(logging, level)(msg)

def update_progress(dev, report):
    # log the progress of the installing process
    do_log(report)

def main():
	print("\nWelcome to Junos Upgrade Tool \n")
	# Request which code to upgrade with
	fileList = getFileList(code_path)
	package = getOptionAnswer("Choose a junos package", fileList)
	package = code_path + package
	# Request IPs for the systems to upgrade
	ips = []
	ips = chooseDevices()
	#host = getInputAnswer("IP Address of the host")
	# Get username and password parameters
	username=getInputAnswer("\nEnter your device username")
	password=getpass(prompt="\nEnter your device password: ")	
	# initialize logging
	logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s:%(name)s: %(message)s')
	logging.getLogger().name = host
	sys.stdout.write('Information logged in {0}\n'.format(logfile))

	# verify package exists
	if (os.path.isfile(package)):
		found = True
	else:
		msg = 'Software package does not exist: {0}. '.format(package)
		sys.exit(msg + '\nExiting program')

	# Loops over all IPs in list to load configuration
	for ip in ips:
	    dev = Device(ip,user=username,password=password)
	    try:
		dev.open()
	    except Exception as err:
		sys.stderr.write('Cannot connect to device: {0}\n'.format(err))
	    else:
		# Increase the default RPC timeout to accommodate install operations
		dev.timeout = 300

		# Create an instance of SW
		sw = SW(dev)

		try:
		    do_log('Starting the software upgrade process: {0}'.format(package))
		    ok = sw.install(package=package, remote_path=remote_path, progress=update_progress, validate=validate)
		except Exception as err:
		    msg = 'Unable to install software, {0}'.format(err) 
		    do_log(msg, level='error')
		else:
		    if ok is True:
			do_log('Software installation complete.')

		# End the NETCONF session and close the connection  
		dev.close()

if __name__ == "__main__":
	main()
