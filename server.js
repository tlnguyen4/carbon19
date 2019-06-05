const http = require('http');
const express = require('express');
const MessagingResponse = require('twilio').twiml.MessagingResponse;
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

Date.prototype.getUnixTime = function() { return this.getTime()/1000|0 };
if(!Date.now) Date.now = function() { return new Date(); }
Date.time = function() { return Date.now().getUnixTime(); }

app.post('/sms', (req, res) => {
    const twiml = new MessagingResponse();

    let message = req.body.Body;

    console.log("message: ", message);

    message = message.split(".");
    const date = message[0].trim().split('/');
    const time = message[1].trim().split(':');
    const todo = message[2].trim();

    console.log("year: ", date[2]);
    console.log("month: ", date[0]);
    console.log("date: ", date[1]);
    
    const remind = new Date(parseInt(date[2]), parseInt(date[0]) - 1, parseInt(date[1]), time[0], time[1], 0, 0).getUnixTime();
    const now = new Date().getUnixTime();

    console.log("reminder: ", remind);
    console.log("now: ", now);
    console.log("diff: ", remind - now);

    setTimeout(function() {
        twiml.message('Reminder to ' + todo);
        res.writeHead(200, { 'Content-Type': 'text/xml' });
        res.end(twiml.toString());
    }, 60000);  
   
});

http.createServer(app).listen(1337, () => {
   console.log('Express server listening on port 1337');
});
