import pytz
import uuid
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from flask import Flask, jsonify, Response
import pprint

app = Flask(__name__)


@app.route('/')
def generate_calendar():
    url = "https://gamesdonequick.com/api/schedule/48"
    response = requests.get(url, timeout=10)
    
    # setup kalender variabele
    cal = Calendar()

    # basiscomponenten ical-format
    cal.add('prodid', 
            '-//SGDQ Calendar//https://gamesdonequick.com/api/schedule/48//')
    cal.add('version', '2.0')

    events = response.json()

    # setup for print checks
    runs = []
    other_items = []
    run_count = 0
    other_count = 0

    for event in events["schedule"]:
        if event["type"] == "speedrun":
            print("event: ", event["display_name"])
            print("start time: ", event["starttime"])
            print("end time: ", event["endtime"], "\n")
            runs += event
            run_count += 1
        else:
            print("other event: ", event["topic"])
            print("duration: ", event["length"], "\n")
            other_items += event
            other_count += 1

    print("runs total: ", run_count)
    print("other total: ", other_count)

    end_datetime = 0

    # create actual calendar events
    for event in events["schedule"]:
        # divide between types
        # runs:
        if event["type"] == "speedrun":
            # get title
            title = event["display_name"]

            # get start time
            start_datetime = datetime.fromisoformat(event["starttime"])

            # get end time
            end_datetime = datetime.fromisoformat(event["endtime"])
            print("event: ", title, "\nstart time: ", start_datetime,
                  "\nend time:", end_datetime, "\n")
            
            # print(start_time.time() , " - " , end_datetime.time())

            # add rest to description
            category = event["category"]
            console = event["console"]
            runner_name = event["runners"][0]["name"]
            if event["runners"][1]:
                for runner in event["runners"]:
                    if runner["name"] == runner_name:
                        continue
                    else:
                        runner_name += (" & ", runner["name"])

            description = ("Category: " + category +
                           "Runner(s): " + runner_name +
                           "\nConsole: " + console)



            # start_time = event["starttime"].split("T")
            # print(start_time[0])
            # print(start_time[1].split("-")[0])
            
            # start_date = start_time[0].split("-")
            # start_year = int(start_date[0])
            # start_month = int(start_date[1])
            # start_day = int(start_date[2])

            # start_time = start_time[1].split(":")
            # start_hour = int(start_time[0])
            # start_minute = int(start_time[1])

            # get end time
            # end_time = event["endtime"].split("T")
            # print(end_time[0])
            # print(end_time[1].split("-")[0])

            # end_date = end_time[0].split("-")
            # end_year = int(end_date[0])
            # end_month = int(end_date[1])
            # end_day = int(end_date[2])

            # end_time = end_time[1].split(":")
            # end_hour = int(end_time[0])
            # end_minute = int(end_time[1])

            # # transform to usable datetime
            # start_datetime = datetime(start_year, start_month, start_day,
            #                           start_hour, start_minute, 0,
            #                           tzinfo=pytz.timezone('America/Minneapolis'))


        # others:
        else:
            # get type and/or topic
            title = event["topic"]
            
            # get duration
            time_split = event["length"].split(":")
            duration = int(time_split[0])*60 + int(time_split[1])
            print("event: ", title, "\nduration: ", duration, " minutes aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n")
            
            # transform to usable datetime
            start_datetime = end_datetime
            end_datetime = start_datetime + timedelta(minutes=duration)

            # add rest to description


        # uid = str(uuid.uuid4())  # willekeurige uid voor event


        # Create an event
        # cal_event = Event()
        # cal_event.add('summary', title)
        # cal_event.add('dtstart', start_datetime)
        # cal_event.add('dtend', end_datetime)
        # cal.add_component(cal_event)

    return Response(response, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
