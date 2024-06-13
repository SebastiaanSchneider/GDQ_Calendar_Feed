"""
Gets JSON of SGDQ event schedule, transforms it into iCal format calendar.
"""
from datetime import datetime, timedelta
import requests
from flask import Flask, jsonify, Response
from icalendar import Calendar, Event


app = Flask(__name__)


@app.route('/')
def generate_calendar():
    """
    Fetch the schedule from the GDQ API, parse the events, 
    and generate an iCalendar file.
    """

    url = "https://gamesdonequick.com/api/schedule/48"

    # Get the JSON from the API
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        events = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except ValueError:
        return jsonify({"error": "Invalid JSON response"}), 500

    # Setup calendar variable
    cal = Calendar()

    # Basic components for iCal format
    cal.add('prodid', '-//SGDQ Calendar//https://gamesdonequick.com/api/schedule/48//')
    cal.add('version', '2.0')

    end_datetime = 0

    # Create actual calendar events
    for event in events["schedule"]:
        # Divide between types of events
        # Runs:
        if event["type"] == "speedrun":
            # Get title and start/end times
            title = event["display_name"]
            start_datetime = datetime.fromisoformat(event["starttime"])
            end_datetime = datetime.fromisoformat(event["endtime"])

            # Add other details to description
            category = event["category"]
            console = event["console"]
            runner_names = " & ".join(runner["name"]
                                      for runner in event["runners"])

            description = (
                f"Category: {category}\n"
                f"Runner(s): {runner_names}\n"
                f"Console: {console}"
            )

        # Other events:
        else:
            # Get event type or topic
            title = event["topic"]

            # Get duration
            time_split = event["length"].split(":")
            duration = (int(time_split[0]) * 60) + int(time_split[1])

            # Transform previous end time to new start and end time
            start_datetime = end_datetime
            end_datetime = start_datetime + timedelta(minutes=duration)

        # Create an event
        cal_event = Event()
        cal_event.add('summary', title)
        cal_event.add('dtstart', start_datetime)
        cal_event.add('dtend', end_datetime)
        if description:
            cal_event.add('description', description)
        cal.add_component(cal_event)

    return Response(cal.to_ical(), mimetype='text/calendar')


if __name__ == '__main__':
    app.run(debug=True)
