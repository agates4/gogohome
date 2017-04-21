from flask import Flask, request, session
from twilio import twiml
from twilio.rest import TwilioRestClient 
from schooldata import SchoolData
from api import LocationFinder

SECRET_KEY = 'randomshit'
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    message = request.values.get('Body', None).lower()
    session.clear()

    # Increment the counter
    counter = session.get('counter', 0)
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    # put your own credentials here 
    ACCOUNT_SID = "ACdf7a6c70d344877633875eb21d0ad140" 
    AUTH_TOKEN = "3b1d1e12e6c147ec8cb6969a6dad0c88" 
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

    # Build our reply
    response = ""
    if counter == 1:
        response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>Welcome! What is your monthly budget? Example: 700</Message></Response>"
    elif counter == 2:
        session['budget'] = message
        response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>How many bedrooms do you need? Example: 2</Message></Response>"
    elif counter == 3:
        session['bathrooms'] = message
        response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>List these in order of importance: School Transportation Healthcare</Message></Response>"
    elif counter == 4:
        message = message.replace(',', '')
        session['importance'] = message

        temp = message.split()
        schoolPriority = 0
        transPriority = 0
        hospPriority = 0
        query = ''
        try:
            if temp[0] == 'school':
                schoolPriority = 1
                query = ''
            elif temp[0] == 'transportation':
                transPriority = 1
                query = 'bus'
            elif temp[0] == 'healthcare':
                hospPriority = 1
                query = 'hospital'

            if temp[1] == 'school':
                schoolPriority = 2
            elif temp[1] == 'transportation':
                transPriority = 2
            elif temp[1] == 'healthcare':
                hospPriority = 2

            if temp[2] == 'school':
                schoolPriority = 3
            elif temp[2] == 'transportation':
                transPriority = 3
            elif temp[2] == 'healthcare':
                hospPriority = 3
        except: 
            schoolPriority=1

        schoolData = SchoolData()
        zipcode = schoolData.get_zip(schoolPriority)
        try:
            api = LocationFinder(int(session['budget']), int(zipcode), str(query))
        except: 
            api=LocationFinder(850,44706,'')
        addresses = api.find_addresses()
        while len(addresses) == 0:
            schoolData = SchoolData()
            zipcode = schoolData.get_zip(schoolPriority)
            try:
                api = LocationFinder(int(session['budget']), int(zipcode), str(query))
            except: 
                api=LocationFinder(850,44706,'')

            addresses = api.find_addresses()
        for address in addresses:
            client.messages.create(
                to=request.values.get('From', None), 
                from_='+12162083656', 
                body=address['name'] + "\n" + address['address'] + '\n' + address['price'] + '\n' + address['number']
            )
        response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>" + '\nAll done! Do you want to give Feedback or Search ?' + "</Message></Response>"
    else:
        if message == "search" or message == "search ":
            session.clear()
            session['counter'] = 1
            response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>Welcome! What is your monthly budget? Example: 700</Message></Response>"
        elif message == "feedback":
            response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>What do you think?</Message></Response>"
        else:
            response = "<?xml version='1.0' encoding='UTF-8'?><Response><Message>If you want to search again just reply with \"Search\"</Message></Response>"
    
    # return "<?xml version='1.0' encoding='UTF-8'?><Response><Message>Thanks for testing our app! We're currently taking it down to diagnose some latency issues, but will be back up soon!</Message></Response>"


if __name__ == '__main__':
    app.run(debug=True, port=5656)
