import todoist
import json
import operator
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, FR

since = datetime.now() + relativedelta(weekday=FR(-2))
since = since.strftime("%Y-%m-%dT00:01")
print since

datecount = {}

user = 'username'
password = 'password'

api = todoist.TodoistAPI()
user = api.login(user,password)

offset = 0
names = {}
items = {}
response = api.get_all_completed_items(since=since,offset=offset)

while len(response['items']) > 0:
	for p in response['projects']:
		names[p] = response['projects'][p]['name']
		items[p] = []
	
	for i in response['items']:
		project = str(i['project_id'])
		items[project].append(i['content'])
	
	offset += len(response['items'])
	response = api.get_all_completed_items(since=since,offset=offset)

for p in items:
	print "# ", names[str(p)].encode('ascii', 'xmlcharrefreplace')
	for i in items[p]:
		print "* ", i.encode('ascii', 'xmlcharrefreplace')
	print
