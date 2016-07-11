import todoist
import json
import re
import operator
import sqlite3
import getopt, sys

from datetime import datetime, timedelta
from spcchart import SpcChart
from operator import itemgetter, attrgetter, methodcaller

datecount = {}

conn = sqlite3.connect("tasks.db")
c = conn.cursor()

online = True
WEB = False
insensitive = False

start = "2016-05-04T00:01"

projectOrder = {}

def orderProject(projectlist, projectid, start=1): # name would be nice, but ID is unique
	project = filter(lambda k: k['id']==projectid, projectlist)[0] # should be unique
	projectOrder[project['id']] = [ start, project['indent'] ]

	children = filter(lambda k: k['parent_id']==projectid, projectlist)
	s = sorted(children, key=lambda x:(x['name']))
	
	start += 1
	for p in s :
		start = orderProject(projectlist, p['id'], start)
	return start

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
     elif o in ("-i", "--insensitivecase"):
         insensitive = True
     else:
         assert False, "unhandled option"

if online:
	api = todoist.TodoistAPI('add your token here')
	offset = 0
	response = api.sync(resource_types=['projects'])
	#names = []
	ids = []
	parents = {}
	parentid = {}
	projects = []
	#labels = []
	#last_indent = 15000000
	offset=0

	# collect all of the project information
	while(len(response['Projects'])) > 0 :
		filtered = filter(lambda k: k['name'] != "Inbox", response['Projects'])
		#for p in response['Projects'] : 
		for p in filtered :
			projects.append( { 'name' : p['name'], 'item_order' : p['item_order'], 'indent' : p['indent'], 'id' : p['id'] } )
		response = api.sync(resource_types=['projects'],offset=offset)
	

	# need to sort the projects by item_order first
	s = sorted(projects, key=lambda x:x['item_order'])
	parent = "" # top level unnamed project
	parents[0] = parent
	parentid[0] = parent
	for p in s:
		parent = parents[p['indent'] - 1]
		parent_id = parentid[p['indent'] - 1]
		parents[p['indent']] = p['name']
		parentid[p['indent']] = p['id']
		ids.append({ "parent_name" : parent, "parent_id" : parent_id, "name" : p['name'], "id" : p['id'], "indent" : p['indent'] })
	s = sorted(ids, key=lambda x:(x['indent'],x['parent_name'],x['name']))

	# recursively process all of top level (indent == 1) projects
	tops = filter(lambda k: k['indent']==1, s)
	start = 1 # "start counting from" used to create the order recursively
	# recurse through the project and create the right order in variable projectOrder
	for t in tops:
		start = orderProject(s, t['id'], start)

	api.projects.update_orders_indents(projectOrder)
	api.commit()
