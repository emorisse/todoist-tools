import todoist
import json
import re
import operator
import sqlite3
import getopt, sys

from datetime import datetime, timedelta

online = True
ignoreCase = False

try:
	opts, args = getopt.getopt(sys.argv[1:], "ois:", ["offline", "ignorecase", "start"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err)  # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
for o, a in opts:
     if o in ("-i", "--ignorecase"):
         ignoreCase = True
     elif o in ("-o", "--offline"):
         online = False
     elif o in ("-s", "--start"):
         start = a
     else:
         assert False, "unhandled option"

labels = []
ids = {}

if online:
	api = todoist.TodoistAPI('goes here!')
	offset = 0
	api.sync()
        response = api.state
	for i in response['labels']:
		if ignoreCase:
			name = i['name'].lower()
			labels.append(name)
			ids[name] = i['id']
		else:
			labels.append(i['name'])
			ids[i['name']] = i['id']

	s=sorted(labels)

	orders = {}
	order = 1
	for l in s:
		#print l
		orders[ids[l]] = order
		order += 1

	#print(orders)
	api.labels.update_orders(orders)
	api.commit()
