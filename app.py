from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests
import os

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/process', speechTimeout='auto')
    gather.say("Hi! This is the VoxaCare assistant. How can I help you today?")
    resp.append(gather)
    resp.redirect('/voice')
    return Response(str(resp), mimetype='text/xml')

@app.route("/process", methods=['POST'])
def process():
    speech_result = request.form.get('SpeechResult', '')
    response_text = "Sorry, I didn't catch that."

    if "book" in speech_result.lower():
        response_text = "Sure, you can book an appointment at calendly.com/jayden-magnalegacy. I've also sent you a text with the link."
        send_sms(request.form.get('From'), "Book here: https://calendly.com/jayden-magnalegacy")
    elif "real person" in speech_result.lower() or "speak to someone" in speech_result.lower():
        vr = VoiceResponse()
        vr.dial(os.environ.get("FORWARDING_NUMBER", "+18588883373"))
        return Response(str(vr), mimetype='text/xml')
    else:
        response_text = f"You said: {speech_result}. I’ll pass this along or you can book now."

    resp = VoiceResponse()
    resp.say(response_text)
    return Response(str(resp), mimetype='text/xml')

def send_sms(to_number, message):
    from twilio.rest import Client
    client = Client(os.environ.get('TWILIO_SID'), os.environ.get('TWILIO_AUTH'))
    client.messages.create(
        to=to_number,
        from_=os.environ.get('TWILIO_PHONE'),
        body=message
    )

@app.route("/", methods=["GET"])
def home():
    return "VoxaCare voicebot is live."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
