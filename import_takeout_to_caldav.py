#!/usr/bin/python

import caldav
import json
import sys
import datetime
from requests.auth import HTTPBasicAuth
import logging

davurl = "https://<user>:<password>@<davserver>/caldav/"

client = caldav.DAVClient(davurl)

gcal_timeparse_string = '%Y-%m-%dT%H:%M:%S.%fZ'
vcal_timeformat_string = '%Y%m%dT%H%M%SZ'

def main(inputfile):
    with open(inputfile, 'r') as f:
        tasks = json.load(f)
        lists = tasks['items']
        for l in lists:
            title = l['title']
            print title
            items = l['items']

            # change this logic, if your calendar .ics files are named
            # differently than the calendar title in the google takeout json
            calendar = caldav.Calendar(client, url=davurl + title + '.ics')

            for t in items:
                ititle = t['title']
                updated = t['updated']
                notes = t.get('notes', "")
                status = t['status']
                completed = t.get('completed', None)
                uid = t['id']

                updated = datetime.datetime.strptime(updated,
                                                     gcal_timeparse_string)
                updated_str = updated.strftime(vcal_timeformat_string)

                if completed:
                    completed = datetime.datetime.strptime(completed,
                                                           gcal_timeparse_string)
                    completed_str = completed.strftime(vcal_timeformat_string)

                print ititle

                todo_str = "BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VTODO\n"
                todo_str += "DTSTAMP:%s\n" % updated_str
                todo_str += "UID:%s\n" % uid
                todo_str += "CREATED:%s\n" % updated_str
                todo_str += "LAST-MODIFIED:%s\n" % updated_str
                todo_str += "SUMMARY:%s\n" % ititle
                todo_str += "DESCRIPTION:%s\n" % notes.replace('\n', '\\n')
                if status == "completed":
                    todo_str += "STATUS:COMPLETED\n"
                    todo_str += "PERCENT-COMPLETE:100\n"
                    if completed:
                        todo_str += "COMPLETED:%s\n" % completed_str
                elif status == "needsAction":
                    todo_str += "STATUS:NEEDS-ACTION\n"
                else:
                    raise ValueError("unknown status: %s" % status)
                todo_str += "END:VTODO\nEND:VCALENDAR"

                calendar.add_todo(todo_str)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "usage: %s [Tasks.json]" % (sys.argv[0])
        sys.exit(1)

    main(sys.argv[1])
