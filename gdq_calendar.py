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
    response = requests.get(url)
    

    # cal = Calendar()

    events = response.json()
    runs = []
    other_items = []
    run_count = 0
    other_count = 0

    for run in events['schedule']:
        if run["type"] == "speedrun":
            print("run: ", run["display_name"])
            runs += run
            run_count += 1
        else:
            print("not run: ", run["topic"])
            other_items += run
            other_count += 1

    print("runs total: ", run_count)
    print("other total: ", other_count)
    # events = 

    # for event in events:
    #     # Extract start time
    #     start_time_tag = event.find(
    #         "div", class_="font-monospace px-4 font-light text-sm lg:text-base min-w-[90px] lg:w-auto")
    #     if not start_time_tag:
    #         continue
    #     start_time_str = start_time_tag.get_text(strip=True)

    #     # Convert start time to a datetime object
    #     try:
    #         start_time = datetime.strptime(start_time_str, "%I:%M %p")
    #     except ValueError:
    #         continue

    #     # Extract title
    #     title_tag = event.find("span", class_="hidden lg:inline")
    #     if not title_tag:
    #         continue
    #     title = title_tag.get_text(strip=True)

    #     # Extract duration
    #     duration_tag = event.find(
    #         "span", class_="font-monospace align-middle text-sm font-normal normal-case text-slate-500 dark:text-slate-400 ml-2")
    #     if not duration_tag:
    #         continue
    #     duration_str = duration_tag.get_text(
    #         strip=True).replace("(Est: ", "").replace(")", "")

    #     # Convert duration to a timedelta object
    #     parts = duration_str.split(':')
    #     if len(parts) == 2:
    #         hours, minutes = map(int, parts)
    #         seconds = 0
    #     elif len(parts) == 3:
    #         hours, minutes, seconds = map(int, parts)
    #     else:
    #         continue
    #     duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    #     # Create an event
    #     cal_event = Event()
    #     cal_event.add('summary', title)
    #     cal_event.add('dtstart', start_time)
    #     cal_event.add('dtend', start_time + duration)
    #     cal.add_component(cal_event)

    return Response(response, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
