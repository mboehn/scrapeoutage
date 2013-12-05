#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re

## This is a list of the places you want to know about
myplaces = [ u'Tjøme', u'Tønsberg', u'Svelvik', u'Sande', u'Hof', u'Holmestrand', u'Horten', u'Re', u'Andebu', u'Lardal', u'Sandefjord', u'Nøtterøy', u'Larvik', u'Stokke']

## URL to dmsweboutagemap
r = requests.get('http://powercompany.example/dmsweboutagemap/Fetch.ashx?markup=0&trusted=check')

lines = r.text.splitlines()

answer = None
total = None

for line in lines:
	a = re.compile ("^outage.add.*")
	if a.match(line):
		ref = line.split (',')
		place = ref[1].replace("'", "")
		faults = ref[2]
		planned = ref[3]
		customers = ref[4].split(')')[0]

		if any (place in s for s in myplaces):
			if customers != '0':
				if answer:
					total += int(customers)
					answer += ", " + place + "[" + faults + "/" + customers + "]"
				else:
					total = int(customers)
					answer = place + "[" + faults + "/" + customers + "]"

print answer + " (" + str(total) + ")"
