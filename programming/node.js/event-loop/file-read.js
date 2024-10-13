const fs = require('fs')
fs.readFile('./events.js', function callback (err, data) {
  console.log('file has been read')
})
