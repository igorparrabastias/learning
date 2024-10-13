const EventEmitter = require('events')

;(() => {
  const myEmitter = new EventEmitter()

  const someFunction = function () {
    console.log('Something has happened!')
  }
  myEmitter.on('Some event', someFunction)

  myEmitter.emit('Some event')
})()

;(() => {
  const EventEmitter = require('events')

  const myEmitter = new EventEmitter()

  let n = 0
  const someFunction = function () {
    n++
    console.log(`Value of n is: ${n}`)
  }

  myEmitter.once('event', someFunction)

  myEmitter.emit('event')
  myEmitter.emit('event')
  myEmitter.emit('event')
})()

;(() => {
  const myEmitter = new EventEmitter()

  const handleError = function (errorCode) {
  // do something about the error
    console.error('Woah, there was an error! \nError code:', errorCode)
  }

  myEmitter.on('error', handleError)

  myEmitter.emit('error', 9)
})()
