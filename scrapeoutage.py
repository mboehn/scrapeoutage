#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Set to True if testing and there only is planned outages:
DO_PLANNED=False

## This is a list of the places you want to know about
myplaces = [ u'Tjøme', u'Tønsberg', u'Svelvik', u'Sande', u'Hof', u'Holmestrand', u'Horten', u'Re', u'Andebu', u'Lardal', u'Sandefjord', u'Nøtterøy', u'Larvik', u'Stokke']

## URL to outagemap
url = 'http://powercompany.example/outagemap/geoserver-api/content/outageTableData.json'


#####################################

import requests
import json
import sys

r = requests.get(url)
r.encoding = 'utf_8'

data = json.loads(r.text)

faultanswer = None
faulttotal = None
plananswer = None
plantotal = None

for mainarea in data['mainAreas']:
	area = mainarea['area']

	if not area in myplaces:
		continue

	faults = mainarea['faultrunning']['nr']
	faultsaffect = mainarea['faultrunning']['customers']
	plans = mainarea['planrunning']['nr']
	plansaffect = mainarea['planrunning']['customers']

	if int(faults):
		if faultanswer:
			faultanswer += ", {} [{}/{}]".format(area, faults, faultsaffect)
			faulttotal += int(faultsaffect)
		else:
			faultanswer = "{} [{}/{}]".format(area, faults, faultsaffect)
			faulttotal = int(faultsaffect)

	if int(plans) and DO_PLANNED:
		if plananswer:
			plananswer += ", {} [{}/{}]".format(area, plans, plansaffect)
			plantotal += int(plansaffect)
		else:
			plananswer = "Planned: {} [{}/{}]".format(area, plans, plansaffect)
			plantotal = int(plansaffect)

if (not faultanswer and not plananswer):
	sys.exit(0)
elif faultanswer:
	print(faultanswer)
	sys.exit(100)
elif plananswer:
	print(plananswer)
	sys.exit(101)
