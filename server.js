const http = require('http');
const express = require('express');
const MessagingResponse = require('twilio').twiml.MessagingResponse;
const { urlencoded } = require('body-parser');
const {Translate} = require('@google-cloud/translate').v2;
const sgMail = require('@sendgrid/mail');

const accountSid = '';
const authToken = '';
const client = require('twilio')(accountSid, authToken);

process.env.GOOGLE_APPLICATION_CREDENTIALS = ""
const translate = new Translate();

const app = express();
const bodyParser = require('body-parser');
app.use(urlencoded({ extended: false }));

const sent = 'sent';
sendsms(sent);
//sendemail(sent);


app.post('/sms', async (req, res) => {
  try{
  const twiml = new MessagingResponse();

  //print sender and message
  console.log(`Incoming message from ${req.body.From}: ${req.body.Body}`);
  
  //{} destructures
  const {Body} = req.body;
  console.log(Body);

  const target = 'es';
  //[..., _] destructures
  const [result, _] = await translate.translate(Body, target);
  console.log(result)

  console.log('send sms'); //send to anyone
  sendsms(result);
  console.log('regular') //reply
  twiml.message(result);
  //console.log('send email');
  //sendemail(result);


  //twiml.message('The Robots are coming! Head for the hills!');

  res.writeHead(200, {'Content-Type': 'text/xml'});
  res.end(twiml.toString());
}
  catch(err){
    console.error(err);
  }
});


exports.handler = function(event, context, callback){
 .then(function() {
         return callback(null, {
                    "statusCode": 200,
                    "headers": {'Content-Type': 'text/xml'},
                    "body":   defaultTwilioSuccess()
                });

            });
}

function sendsms(body){
client.messages
  .create({
     body: body,
     from: '',
     to: ''
   })
  .then(message => console.log(message.sid));
}

function sendemail(body){
ru = '';
per = '';
console.log("sending");
const msg = {
  to: ru,
  from: per,
  subject: 'Sending with SendGrid is Fun',
  text: body,
  html: '',
};
sgMail.send(msg);
}


//set up express server
http.createServer(app).listen(1337, () => {
  console.log('Express server listening on port 1337');
});
