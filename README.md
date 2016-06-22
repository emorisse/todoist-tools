# Repository Contents
*todoist.summary.py* - Creates a markdown summary for all items completed since last Friday.  
*todoist.completedtasks.py* - Gives you the how many tasks you've completed every day
	* relies on tasks.db - a sqlite db for storage
*projects.with.no.next.py* - gives a list of projects that have no "@next" label
*labelReorder.py* - reorders all of your labels alphabetically
	optional flag:
	* -i, --ignorecase: use this flag to ignore upper/lower case in alpha sort  
*controlcharts.R* - R language code to generate the control charts.
	* creates charts like exampleplot.png
