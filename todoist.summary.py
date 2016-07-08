import todoist
import json
import operator
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, FR

if datetime.today().weekday() == 4: # today is Fri, so we need previous Fri
	last_friday = -2
else:
	last_friday = -1

since = datetime.now() + relativedelta(weekday=FR(last_friday))
since = since.strftime("%Y-%m-%dT00:01")

#since = "2016-06-24T00:01"

datecount = {}

api = todoist.TodoistAPI('put your API key here!')

offset = 0
names = {}
items = {}
response = api.get_all_completed_items(since=since)

while len(response['items']) > 0:
	for p in response['projects']:
		names[p] = response['projects'][p]['name']
		if not p in items:
			items[p] = []
	
	for i in response['items']:
		project = str(i['project_id'])
		items[project].append(i['content'])
		offset += 1
	
	response = api.get_all_completed_items(since=since,offset=offset)

for p in names:
	print "# ", names[p].encode('ascii', 'xmlcharrefreplace')
	for i in items[p]:
		print "* ", i.encode('ascii', 'xmlcharrefreplace')
	print
