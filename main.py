import os
import six
from twilio.rest import Client
from keys import *
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
from google.cloud import translate_v2 as translate

print("running main.py")
sampletext = "+17322895888, +17326518289, +17325551023***\n/Hello, how are you?/\n***span, chin, hebr"

app = Flask(__name__)

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\2000r\\Documents\\translate\\translatetalk-1582409537821-c9cffd188eaf.json"
translate_client = translate.Client()

def detect(text):
	result = translate_client.detect_language(text)
	print('Text: {}'.format(text))
	print('Confidence: {}'.format(result['confidence']))
	print('Language: {}'.format(result['language']))

def translate(text, target):
	text = bytes(text, 'utf-8')
	if isinstance(text, six.binary_type):
		text = text.decode('utf-8')
		# text = text.decode('utf-8')
		result = translate_client.translate(
    text, target_language=target)
		print(u'Text: {}'.format(result['input']))
		print(u'Translation: {}'.format(result['translatedText']))
		print(u'Detected source language: {}'.format(
    result['detectedSourceLanguage']))
		total = result['translatedText']
		return total


#store securely
#https://www.twilio.com/docs/usage/secure-credentials

@app.route("/sms", methods=['GET', 'POST'])

def receiveSMS():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()
    body = request.values.get('Body', None)
    #print(body)

    # Add a message

    nums = getNums(body)
    text = getText(body)
    langs = getLangs(body)

    same = False;

    if(nums != '000' and langs != '000'):
    	nsize = len(nums)
    	lsize = len(langs)
    	if(nsize == lsize):
    		same = True;

    print(langs)
    if((nums == '000' or text == '000' or langs == '000') or same == False):
    	resp.message("Sorry, it looks like something didn't work! " +
    		"You might have put in an incorrect amount of phone numbers or languages, " +
    		"made a typo, or forgotten a delimiter. Please try again.")
    else:
	    keys = getDict(nums, langs)
	    count = -1
	    for n in nums:
	        count += 1
	        target = langs[count]
	        target = target[:2]
	        print(target)
	        result = translate(text, target)
	        print("result: ", result)
	        message = client.messages \
	                .create(
	                     body=result,
	                     from_='+14253812112',
	                     to=nums[count]
	                 )
	    detect(text)
	    print("received")


    return str(resp)

def getNums(sampletext):
	try:
		numpattern = r"([\+]\d{11}[,]?[\s]?)+[\s]?((\*){3})"
		numf = re.search(numpattern, sampletext)
		num = numf.group()
		num = num.replace('*', '')
		num = num.replace(' ', '')
		numlist = num.split(',')
	except AttributeError as error:
		numlist = '000'
		print('errornums')
	return numlist

def getText(sampletext):
	try:
		bodytext = re.search('.*?(/(.*)/)', sampletext)
		body = bodytext.group()
		body = body.replace('/', '')
	except AttributeError as error:
		body = '000'
		print('errorbody')
	return body

def getLangs(sampletext):
	langtext = re.search('[(\*){3}][\s]?([A-Za-z]{4}[,]?[\s]?)+', sampletext)
	try:
		langcount = 0
		lang = langtext.group()
		lang = lang.replace('*', '')
		lang = lang.replace(' ', '')
		langlist = lang.split(',')
	except AttributeError as error:
		langlist = '000'
		print('errorlang')
	return langlist

def getDict(numlist, langlist):
	outgoing = {}
	for n, l in zip(langlist, numlist):
		outgoing.setdefault(l, []).append(n)
	return outgoing

if __name__ == "__main__":
    app.run(debug=True)