// Download the helper library from https://www.twilio.com/docs/node/install
// Your Account Sid and Auth Token from twilio.com/console
// DANGER! This is insecure. See http://twil.io/secure
const accountSid = 'ACfb5ac0f6ad89092173c8213cb09bf6c8';
const authToken = '69bbdb9ee5181c2cd5f55054979d1bc6';
const client = require('twilio')(accountSid, authToken);

client.messages
  .create({
     body: 'This is testing the sending method.',
     from: '+12063394673',
     to: '+12063137687'
   })
  .then(message => console.log(message.sid));
