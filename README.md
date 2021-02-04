This program checks a Calendly calendar for appointments and sends a text message when one is found.

## Prerequisites
In order to get a text message when an appointment is found, this program utilizes Twilio. You will need to
set up a Twilio API Key/Secret combination. You will start your free trial with around $15 in credit which is enough to send 
a few hundred text messages.
https://www.twilio.com/console

Once you have set up your Twilio API Key, copy the SID and Secret into a file called `.env`:

```
CLIENT_ID=<SID>
CLIENT_SECRET=<SECRET>
```

If you would like to choose a different Calendly calendar than the ones in `main.py`, you will need to change the properties of the `calendar` map and find the appropriate base URL. (You can check the network tab to see what API calls the calendly calendar is making, and strip off the query string parameters because we'll add our own). 

Once the calendar is the one you want, run
`python main.py`

## Other customizable parameters:
- How long should the program sleep before making the next request
