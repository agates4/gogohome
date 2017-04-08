from flask import Flask, request, session
from twilio import twiml

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
    response = ""
    if counter == 1:
        response = 'Welcome! What is your monthly budget? Example: 100'
    elif counter == 2:
        response = 'How many bedrooms do you need? Example: 2'
    elif counter == 3:
        response = 'How many bathrooms do you need? Example: 1'
    elif counter == 4:
        response = 'What is more important to you? Schools, or Transportation?'
    elif counter == 5:
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