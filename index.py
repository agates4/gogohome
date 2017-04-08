from flask import Flask, request, session
from twilio import twiml
from schooldata import SchoolData
from api import LocationFinder

SECRET_KEY = 'randomshit'
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    message = request.values.get('Body', None).lower()
    # session.clear()

    # Increment the counter
    counter = session.get('counter', 0)
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    # Build our reply
    # paramArray contains the user responses, in the order of questions asked.
    response = ""
    if counter == 1:
        response = 'Welcome! What is your monthly budget? Example: 100'
    elif counter == 2:
        session['budget'] = message
        response = 'How many bedrooms do you need? Example: 2'
    elif counter == 3:
        session['bedrooms'] = message
        response = 'How many bathrooms do you need? Example: 1'
    elif counter == 4:
        session['bathrooms'] = message
        response = 'List these in order of importance: Schools Transportation Hospitals'
    elif counter == 5:
        session['importance'] = message
        temp = message.split()
        schoolPriority = 0
        transPriority = 0
        hospPriority = 0
        if temp[0] == 'schools':
            schoolPriority = 1
        elif temp[0] == 'transportation':
            transPriority = 1
        elif temp[0] == 'hospitals':
            hospPriority = 1

        if temp[1] == 'schools':
            schoolPriority = 2
        elif temp[1] == 'transportation':
            transPriority = 2
        elif temp[1] == 'hospitals':
            hospPriority = 2

        if temp[2] == 'schools':
            schoolPriority = 3
        elif temp[2] == 'transportation':
            transPriority = 3
        elif temp[2] == 'hospitals':
            hospPriority = 3

        print(schoolPriority)
        print(transPriority)
        print(hospPriority)
        schoolData = SchoolData()
        zipcode = schoolData.get_zip(schoolPriority)
        api = LocationFinder(session['budget'], zipcode, schoolPriority)
        response = 'All done! Do you want to search again? Yes, or No?'
    else:
        if message == "yes":
            session.clear()
            session['counter'] = 1
            response = 'Welcome! What is your monthly budget? Example: 100'
        else:
            response = 'If you want to search again just reply with "Yes"'
    
    # Put it in a TwiML response
    resp = twiml.Response()
    resp.message(response)
    
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True, port=5656)