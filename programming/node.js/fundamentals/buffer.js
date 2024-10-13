/*
The Buffer class is based on JavaScript’s
Uint8Array. To put it simply, we can think of
Buffer objects as arrays that only contain
integers from 0 to 255.

While we did state that buffers only store data
as integers, when we output a buffer, it is
represented in hexadecimal notation. This makes
it easier and shorter to read.

The Buffer class and its methods are very useful;
however, being a low-level API, we rarely use it
directly.
*/

const buf1 = Buffer.alloc(10)
console.log(buf1)

const buf2 = Buffer.alloc(5, 15)
console.log(buf2)

// Another way of creating a Buffer is by using
// the Buffer.allocUnsafe method, as it is done in
// line 7 of the code. This, as the name suggests,
// is unsafe as it returns a Buffer that may or may
// not be empty. However, this is faster than the
// safe method.
const buf3 = Buffer.allocUnsafe(10)
console.log(buf3)

buf3.fill(1)
console.log(buf3)

buf2.write('abcedf')
console.log(buf2)

const buf4 = Buffer.from([265, 6.5, -255, '7'])
console.log(buf4)

const buf5 = Buffer.from('Hello world')
console.log(buf5)

console.log(buf5.toString())
