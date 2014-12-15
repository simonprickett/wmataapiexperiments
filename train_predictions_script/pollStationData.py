#####
# Script to poll API data for DC Metro station
#
# Author: Simon Prickett
#####

import json
import os
import requests
import sys
import time

#####
# Query the WMATA API for data for the station represented
# by stationCode e.g. N06 = Reston Wiehle East
#####
def getStationData(stationCode, apiKey):
	url = 'https://wmataapibeta.azure-api.net/StationPrediction.svc/json/GetPrediction/' + stationCode + '?api_key=' + apiKey
	res = requests.get(url)
	return res.json()

#####
# Display error telling user to set up their WMATA_API_KEY
# environment variable
#####
def needToSetApiKey():
	print 'You need to set an environment variable:'
	print 'WMATA_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	print 'Before you can run this script.'
	exit(1)

#####
# Display usage error message
#####
def usage():
	print 'This script requires 2 parameters, a station code and a number of times to'
	print 'query for data and a filename to store the results in.'
	print 'Example: ' + sys.argv[0] + ' N06 2000'
	exit(1)

#####
# Entry point
#####
apiKey = os.environ.get('WMATA_API_KEY', '')
if (len(apiKey) == 0):
	needToSetApiKey()
	
if (len(sys.argv) == 4):
	# Got the right number of arguments, is the second one an integer
	numSamples = 0
	try:
		numSamples = int(sys.argv[2])
		currentSample = 1
		print 'Will take ' + sys.argv[2] + ' samples for ' + sys.argv[1] + ' and store in ' + sys.argv[3]
		f = open(sys.argv[3], 'w')		
		f.write('[\n')

		while (currentSample <= numSamples):
			print sys.argv[1] + ' ' + str(currentSample) + ' of ' + str(numSamples)
			json.dump(getStationData(sys.argv[1], apiKey), f)
			currentSample += 1

			# Do we need a comma or is this the last iteration?
			if (currentSample <= numSamples):
				f.write(',')

			f.write('\n')
			f.flush()
			time.sleep(60)

		f.write(']')
		f.close()
	except ValueError:
		usage()		
else:
	# Incorrect invocation
	usage()
