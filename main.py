import requests
from twilio.rest import Client
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client = Client(CLIENT_ID, CLIENT_SECRET)
covid_calendar = {
    "name": "Eric's RX Covid Vaccines",
    "base_url": "https://calendly.com/api/booking/event_types/EBAXZXNO5XL6LLRJ/calendar/range?timezone=America%2FNew_York&diagnostics=false"}

lawyers_calendar = {
    "name": "Lawyers",
    "url": "https://calendly.com/api/booking/event_types/DDEEEBW4KOBI57MM/calendar/range?timezone=America%2FNew_York&diagnostics=false&range_start=2021-02-01&range_end=2021-02-28"}

def send_success_sms(calendar, start_time):
	# change the "from_" number to your Twilio number and the "to" number
	# to the phone number you signed up for Twilio with, or upgrade your
	# account to send SMS to any phone number
    calendar_name = calendar['name']
    client.messages.create(to="+14842011537",
                           from_="+16178632712",
                           body= f'Found an appointment for {calendar_name}!! Appointment time: {start_time}')

def format_date_range():
    start = datetime.now()
    end = start + timedelta(days = 31)
    
    date_format = "%Y-%m-%d"
    formatted_start = datetime.strftime(start, date_format)
    formatted_end = datetime.strftime(end, date_format)
    return f'&range_start={formatted_start}&range_end={formatted_end}'
    
def check_next_four_weeks():
    calendar = covid_calendar

    request_url = calendar['base_url'] + format_date_range()
    print("Request URL:", request_url)
    resp = requests.get(request_url)
    resp_obj = resp.json()
    days = resp_obj['days']

    try:
        first_available_day = next(day for day in days if day['status'] == 'available')
        spots_on_day = first_available_day['spots']
        try:
            first_available_slot = next(slot for slot in spots_on_day if slot['status'] == 'available')
            first_available_time = datetime.strptime(first_available_slot['start_time'], "%Y-%m-%dT%H:%M:%S%z")
            first_time_formatted = datetime.strftime(first_available_time, "%b %d, %Y at %H:%M%p")
            send_success_sms(calendar, first_time_formatted)
            return True
        except StopIteration:
            print("No slots found with availability")

    except StopIteration:
        print("No days found with availability")

    return False

def keep_checking():
    result = check_next_four_weeks()

    if result == True:
        # found appointment, wait a longer time to check again
        print(f'{datetime.now().strftime("%H:%M:%S")}: Found an appointment. Will wait 30 minutes to check again.')
        time.sleep(60 * 30)
        keep_checking()
    else:
        # no appointment found, keep checking every minute:
        print(f'{datetime.now().strftime("%H:%M:%S")}: No appointment found, checking again in a minute.')
        time.sleep(60)
        keep_checking()

keep_checking()
