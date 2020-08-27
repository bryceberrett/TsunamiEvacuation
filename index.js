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

// Make the temporary directory where we store the files we receive from the server

var dir = './tmp';

if (!fs.existsSync(dir)){
    fs.mkdirSync(dir);
}

// These are the fields that we are gathering from the user

const fields = {
	//"Mewtwo": "text",
	//"Celebi": "file",
	//"Lugia": "file",
	//"Ho-oH": "text"
	"DEM": "file",
	"Roads": "file",
	"Evacuation Elevation": "text"
}

// Create lists of names and field types

const keys = Object.keys(fields)
const textKeys = Object.keys(fields).filter(key => fields[key] != "file")
const fileKeys = Object.keys(fields).filter(key => fields[key] == "file")

//Serve the main page

app.get('/', async (req, res) => {
	res.send(mainPage({'keys': keys, 'types':fields}))
})

app.post('/', (req, res) => {
	ans = ""

	// Download the data for the file inputs
	
	for(k of fileKeys){
		var filename = k;
		var data = req.files[k].data
		var fd = fs.openSync("./tmp/" + filename, 'w')
		fs.writeSync(fd, data)
		fs.closeSync(fd)
		ans += data
	}

	// Put all of the information necessary into a Python script

	var pyDictPath = "./tmp/params.py" 

	// Process these with a python script
	
	// Clear the temporary directory

	fs.unlinkSync(pyDictPath)

	for(k of fileKeys){
		var path = "./tmp/" + k
		fs.unlinkSync(path)
	}


	// Send them back the result of the QGIS script
	res.send("Success")
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
