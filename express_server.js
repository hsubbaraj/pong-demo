'use strict'

const express = require('express')
const bodyParser = require('body-parser')

// Create a new instance of express
const app = express()

// Tell express to use the body-parser middleware and to not parse extended bodies
app.use(bodyParser.urlencoded({
    extended: false
}))
app.use(bodyParser.json())
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "*");
  next();
});


// Route that receives a POST request to /sms
app.post('/', function (req, res) {
  const body = req.body
  res.set('Content-Type', 'text/plain')
  res.send(`You sent: ${body} to Express`)
})

// Tell our app to listen on port 3000
app.listen(8080, function (err) {
  if (err) {
    throw err
  }

  console.log('Server started on port 8080')
})