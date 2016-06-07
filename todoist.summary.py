import todoist
import json
import re
import operator
import sqlite3
import csv
import sys
from datetime import datetime, timedelta
from spcchart import SpcChart
from dateutil.relativedelta import relativedelta, FR

since = datetime.now() + relativedelta(weekday=FR(-1))
since = since.strftime("%Y-%m-%dT00:01")

datecount = {}

user = 'username'
password = 'password'

api = todoist.TodoistAPI()
user = api.login(user,password)
response = api.get_all_completed_items(since=since, limit=34000)

names = {}
items = {}

for p in response['projects']:
	names[p] = response['projects'][p]['name']
	items[p] = []

csvout = csv.writer(sys.stdout)
for i in response['items']:
	project = str(i['project_id'])
	items[project].append(i['content'])

for p in items:
	print "# ", names[str(p)].encode('ascii', 'xmlcharrefreplace')
	for i in items[p]:
		print "* ", i.encode('ascii', 'xmlcharrefreplace')
	print
