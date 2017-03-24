import todoist
import json
import re
import operator
import getopt, sys

from datetime import datetime, timedelta

online = True
WEB = False

filter = '@next'
token = 'goes here!'

try:
	opts, args = getopt.getopt(sys.argv[1:], "ow", ["offline", "web"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err)  # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
for o, a in opts:
     if o in ("-w", "--web"):
         WEB = True
     elif o in ("-o", "--offline"):
         online = False
     else:
         assert False, "unhandled option"

yesnext = {}
if online:
	api = todoist.TodoistAPI(token)
        api.sync()
	response = api.query([filter])
	for p in response[0]['data']:
		if yesnext.has_key(p['project_id']):
			yesnext[p['project_id']] += 1
		else:
			yesnext[p['project_id']] = 1
	offset = 0
	for p in api.state['projects']:
		if yesnext.has_key(p['id']) or p['is_archived'] == 1:
			1
		else:
			print "* ", p['name']
                        #print p
	

