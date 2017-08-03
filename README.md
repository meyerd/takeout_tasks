Takeout your Tasks
==================

This script can be used to take the .json data, that
can be downloaded from Google takeout, when ticking the
"Tasks" export.

Howto
-----

1) Download the .zip file containing your tasks
2) Unzip and find the Tasks.json file
3) Create a tasklist/calendar for each list you had in google
   (Note: The tasklisk <name>.ics has to be exactly the same as
   the listname in google. If not, you have to adjust the calendar
   naming logic in the script file)
4) Adjust the `caldav_url` in the script file
5) Run the script. It should print the task title for every task
   processed.

This script was tested against a radicale caldav server so far.
