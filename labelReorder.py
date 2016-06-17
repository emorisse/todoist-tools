import todoist
import json
import re
import operator
import sqlite3
import getopt, sys

from datetime import datetime, timedelta

online = True
ignoreCase = False

start = "2016-05-04T00:01"

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
	api = todoist.TodoistAPI()
	user = 'username'
	password = 'password'
	user = api.login(user,password)
	offset = 0
	response = api.sync(resource_types=['labels'])
	#response = api.get_completed_items(project_id=128244053)
	#response = api.get_all_completed_items(since=start,limit=34000) # seems to only get 200
	#print response
	#exit
	while len(response['Labels']) > 0:
		for i in response['Labels']:
			if ignoreCase:
				name = i['name'].lower()
				labels.append(name)
				ids[name] = i['id']
			else:
				labels.append(i['name'])
				ids[i['name']] = i['id']
		offset += len(response['Labels'])
		response = api.sync(resource_types=['labels'], offset=offset)
		

	s=sorted(labels)
	#print s
	#print ids

	orders = {}
	order = 1
	for l in s:
		#print l
		orders[ids[l]] = order
		order += 1

	#print orders
	api.labels.update_orders(orders)
	api.commit()
