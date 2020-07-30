var express = require('express')
var spawn = require('child_process').spawnSync
var fs = require('fs')
var path = require('path')

var app = express()

// Middleware
var fileUpload = require('express-fileupload')
app.use(express.urlencoded({
  extended: true
}))
app.use(fileUpload())

const port = 8000

app.get('/', async (req, res) => {
  res.sendFile(path.join(__dirname + '/page.html'))
})

app.post('/', (req, res) => {
  var filename = 'test.py'
  var data = req.files.inputFile.data
  var fd = fs.openSync(filename, 'w')
  fs.writeSync(fd, data)
  fs.closeSync(fd)
  var process = spawn('/usr/bin/python3', [filename])
  var result = process.stdout
  console.log(result)
  res.end(result)
  // res.send('test')
})

app.listen(port, err => {
  if (err) {
    console.log(err)
  }
  console.log(`Server listening on ${port}`)
})
