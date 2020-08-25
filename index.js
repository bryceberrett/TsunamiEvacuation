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

// PUG template setup

const pug = require('pug')
const mainPage = pug.compileFile('page.pug')

// These are the fields that we are gathering from the user

const fields = {
	"Mewtwo": "text",
	"Celebi": "file",
	"Lugia": "file",
	"Ho-oH": "text"
}

// Create lists of names and field types

const keys = Object.keys(fields)


//Serve the main page

app.get('/', async (req, res) => {
	console.log(Object.keys(fields))
	res.send(mainPage({'keys': keys, 'types':fields}))
})

app.post('/', (req, res) => {
	ans = ""
	//fields.forEach(element => {
		//ans += element + ": " + req.body[element] + "\n"
	//})

	res.send(ans)
})

// Handle the posted result

//app.post('/', (req, res) => {
  //var filename = 'test.py'
  //var data = req.files.inputFile.data
  //var fd = fs.openSync(filename, 'w')
  //fs.writeSync(fd, data)
  //fs.closeSync(fd)
  //var process = spawn('/usr/bin/python3', [filename])
  //var result = process.stdout
  //console.log(result)
  //res.end(result)
  //// res.send('test')
//})

app.listen(port, err => {
  if (err) {
    console.log(err)
  }
  console.log(`Server listening on ${port}`)
})
