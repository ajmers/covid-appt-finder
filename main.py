from html.parser import HTMLParser
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from twilio.rest import Client
from datetime import datetime
import requests
import time

calendly_url = "https://calendly.com/eric-s-covid-vaccine/covid-vaccine?month=2021-02"

# we import the Twilio client from the dependency we just installed

# the following line needs your Twilio Account SID and Auth Token
client = Client("client_id", "client_secret")

def send_success_sms(url):
	# change the "from_" number to your Twilio number and the "to" number
	# to the phone number you signed up for Twilio with, or upgrade your
	# account to send SMS to any phone number
	client.messages.create(to="+14842011537",
                       from_="+16178632712",
                       body=f'Found an appointment on calendar {url}!!')
        

def send_failure_sms():
	# change the "from_" number to your Twilio number and the "to" number
	# to the phone number you signed up for Twilio with, or upgrade your
	# account to send SMS to any phone number
	client.messages.create(to="+14842011537",
                       from_="+16178632712",
                       body="No appointments found!")


def check_for_no_dates_found_button(url, sleeptime):
	session = HTMLSession()

	r = session.get(url)

	r.html.render()  # this call executes the js in the page

	no_dates_found_button =  r.html.find('.calendar-no-dates-button')
	if len(no_dates_found_button) == 1:
		print(f'{datetime.now().strftime("%H:%M:%S")}: no dates available on calendar {url}')
		time.sleep(sleeptime)	
		check_for_no_dates_found_button(url)
	else:
		print(f'Found a date on calendar {url}!')
		send_success_sms()


check_for_no_dates_found_button(calendly_url, 5 * 60) 
