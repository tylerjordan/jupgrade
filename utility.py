# File: utility.py
# Author: Tyler Jordan
# Modified: 12/15/2014
# Purpose: Assist CBP engineers with Juniper configuration tasks

import sys
import fileinput
import glob
import code

from os import listdir
from os.path import isfile, join

user = 'root'
passwd = 'ah64dlb'

#--------------------------------------
# ANSWER METHODS
#--------------------------------------
# Method for asking a question that has a single answer
def getOptionAnswer(question, options):
	answer = ""
	loop = 0;
	while not answer:
		print question + '?:\n'
		for option in options:
			loop += 1
			print '[' + str(loop) + '] -> ' + option
		answer = raw_input('Your Selection: ')
		if answer >= "1" and answer <= str(loop):
			index = int(answer) - 1
			return options[index]
		else:
			print "Bad Selection"
			answer = ""

# Method for asking a question, with multiple options, and multiple answers
def getMultiAnswer(question, options):
	answer = ""
	answers = {}
	loop = 0;
	while not answer:
		print question + '?:\n'
		for option in options:
			loop += 1
			print '[' + str(loop) + '] -> ' + option
		print '[x] -> Submit Selections'
		answer = raw_input('Your Selection: ')
		if answer >= "1" and answer <= str(loop):
			index = int(answer) - 1
			answers.append(options[index])
		elif answer == "x":
			return answers
		else:
			print "Bad Selection"
			answer = ""

# Method for asking a user input question
def getInputAnswer(question):
	answer = ""
	while not answer:
		answer = raw_input(question + '?: ')
	return answer
	
# Method for asking a Y/N question
def getYNAnswer(question):
	answer = ""
	while not answer:
		answer = raw_input(question + '?(y/n): ')
		if answer == 'Y' or answer == 'y':
			answer = 'y'
		elif answer == 'N' or answer == 'n':
			answer = 'n'
		else:
			print "Bad Selection"
			answer = ""
	return answer

# Return list of files from a directory
def getFileList(mypath):
	fileList = []
	for afile in listdir(mypath):
		if isfile(join(mypath,afile)):
			fileList.append(afile)
	return fileList

# Method for requesting IP address target
def getTarget():
	print 64*"="
	print "= Scan Menu                                                    ="
	print 64*"="
	# Loop through the IPs from the file "ipsitelist.txt"
	loop = 0
	list = {};
	for line in fileinput.input('ipsitelist.txt'):
		# Print out all the IPs/SITEs
		loop += 1
		ip,site = line.split(",")
		list[str(loop)] = ip;
		print '[' + str(loop) + '] ' + ip + ' -> ' + site.strip('\n')
		
	print "[c] Custom IP"
	print "[x] Exit"
	print "\n"

	response = ""
	while not response:
		response = raw_input("Please select an option: ")
		if response >= "1" and response <= str(loop):
			return list[response]
		elif response == "c":
			capturedIp = ""
			while not capturedIp:
				capturedIp = raw_input("Please enter an IP: ")
				return capturedIp
		elif response == "x":
			response = "exit"
			return response
		else:
			print "Bad Selection"
			
# Common method for accessing multiple routers
def chooseDevices():
	# Define the routers to deploy the config to (file/range/custom)
	print "**** Configuration Deployment ****"
	method_resp = getOptionAnswer('How would you like to define the devices', ['file', 'range', 'custom'])
	ip_list = []
	# Choose a file from a list of options
	if method_resp == "file":
		print "Defining a file..."
		path = '.\ips\*.ips'   
		files=glob.glob(path)   
		file_resp = getOptionAnswer('Choose a file to use', files)
		
		# Print out all the IPs/SITEs
		for line in fileinput.input(file_resp):
			ip_list.append(line)		
		
	# Define a certain range of IPs
	elif method_resp == "range":
		print "Defining a range..."
		
	# Define one or more IPs individually
	elif method_resp == "custom":
		print 'Define using /32 IP Addresses'
		answer = ""
		while( answer != 'x' ):
			answer = getInputAnswer('Enter an ip address (x) to exit')
			if( answer != 'x'):
				ip_list.append(answer)
		
	# Print the IPs that will be used
	loop = 1;
	for my_ip in ip_list:
		print 'IP' + str(loop) + '-> ' + my_ip
		loop=loop + 1

	return ip_list
	
# Writes the listDict to a file with CSV format
def listDictCSV(myListDict, fileName, keys):
	
	try:
		f = open(fileName, 'w')
	except:
		print "Failure opening file in write mode"
	
	# Write all the headings in the CSV
	for akey in keys[:-1]:							# Runs for every element, except the last
		f.write(akey + ",")							# Writes most elements
	f.write(keys[-1])								# Writes last element
	f.write("\n")
	
	for part in myListDict:
		for bkey in keys[:-1]:
			# print "Key: " + key + "  Value: " + part[key]
			f.write(part[bkey] + ",")
		f.write(part[keys[-1]])
		f.write("\n")
	f.close()
	print "Completed writing commands."

# Check if file is in "set" format
