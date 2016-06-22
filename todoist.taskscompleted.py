import todoist
import json
import re
import operator
import sqlite3
import getopt, sys

from datetime import datetime, timedelta
from spcchart import SpcChart

datecount = {}

conn = sqlite3.connect("tasks.db")
c = conn.cursor()

online = True
WEB = False

start = "2016-05-04T00:01"

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

if online:
	api = todoist.TodoistAPI('Hey! Put your API token here!')
	offset = 0
	response = api.get_all_completed_items(since=start,limit=34000) # seems to only get 200
	while len(response['items']) > 0:
		for i in response['items']:
		   # Tue 10 May 2016 17:03:14 +0000
		   date = i['completed_date']
		   d = re.sub(r'\s[+-]\d\d\d\d$',r'',date)
		   # fix TZ from GMT to laptop local
		   d = datetime.strptime(d, "%a %d %b %Y %H:%M:%S")
		   d -= timedelta(hours=4)
		   d = d.date().isoformat()
		   if datecount.has_key(d):
		      datecount[d] += 1
		   else:
		      datecount[d] = 1
		offset += len(response['items'])
		response = api.get_all_completed_items(offset=offset,since=start)

	
	s= sorted(datecount.items(), key=operator.itemgetter(0),reverse=False)
	
	sql = 'INSERT OR REPLACE INTO items (date, count) VALUES (?, MAX(COALESCE((SELECT count FROM items WHERE date = ?), 0), ?));'
	
	for date,count in s:
	   c.execute(sql, (date, date, count))
	conn.commit()

c.execute("select date, count from items order by date")
a = c.fetchall()

items = []
for item in a:
	items.append(item[1])
print items

if WEB:
	c = SpcChart(items, title="Widget Quality",filename="larry")
	c.render_to_file()
