## L1.1: Review of Modern Application Development - I and what next?

Who coined the term "JAMStack"?
=> Mathias Biilmann

---

## L1.2: JavaScript Origins and Overview

DOM => Document Object Model

Which of the following is true regarding java applet?

- It is a special program that can be run by a browser's java virtual machine.
- [❌] It is a programming language.
- Applets are written in java.
- It can be embedded in HTML documents.

Which of the following is the correct way to embed an applet in an HTML document, assuming that the java byte code file "appletdemo.class" is kept in the same directory as the HTML document?

- `<applet code="appletdemo.class"> </applet>`
- `<applet code = "appletdemo" > </applet>`

Which of the following is the correct usage of "alt" attribute in the <applet> tag in an HTML document?

- It is used to display alternative text in case the browser does not support Java

---

## L1.3: Basics of JavaScript

### Statement and Expression

-> Piece of code that can be executed
-> Piece of code that can be executed to obtain a value to be erturned

### Data Types

-> boolean number string, bigint, symbol [undefined and null are primitive data types]
-> Objects (can have function -> methods)
-> Functions (can be handled like objects) (can have associated objects)

Which of the following encoding does a JavaScript engine use in general?

- UTF-16

Which of the following have a block-level scope in JavaScript language?

- let
- const

What is ECMAScript?

- It is a JavaScript standard.
- It was designed to ensure the inter-portability of webpages across the browsers.

---

## L1.4: JavaScipt - Identifiers, Expressions, and Variables

### Operators and coercion

```js
3   +  4  => 7
'3' + '4' => '34'
3   + '4' => '34'
'3' +  4  => '34'
'3' * '4' => 12
```

```js
3==4
3==3

3=='3'
3==='3'
3===3

undefined == null
undefined === null

```

Prefer `===`

---

## L1.5: JavaScript - Control Flow and Functions

`undefined`:
- not initialized
- unknoiewn state

`null`
- excplicit non value


`const`
- immutable object
- values cannot be changed once reassigned
- object, keys, values can be changes

`let`
- variable that can be updated


```js
for(const x = 0; x < 5; x++) {
  ...
}
for(let x = 0; x < 5; x++) {
  ...
}

const v = [1,2,3,4]
for(const x in v) {
  x : 0, 1, 2, 3
}
const v = [1,2,3,4]
for(const x of v) {
  x : 1,2,3,4
}
```

### Functions

functoin add(x, y) {
  ...
}

--OR--

// returns anonymous func assign to add
let add = function(x, y) {

}

--OR--


let add = (x, y) => x + y;


let x = function() {  } // anon function

(function() {}()); // declare and invoke

IIFE -> Immedistely invoked function expression/execution

`typeof` -> return type of variable

```js
const x
=> Uncaught SyntaxError: Missing initializer in const declaration
```


```js
const x = { a : 1 };

obj.double = function(i) { this.a = i * this.a }

obj.double(2)

x === { a: 2}
```

---

## L1.6: JavaScript - DOM API

Inputs ->
Outputs ->


```js
let d1 = document.getElementById('');
d1.innerHTML = '';

d1.addEventListener('click', (e) => {
  x++;
  d1.innerHTML = '';


  d1.style.fontSize = '';
});

```


```js
async function x() {
  await new Promise(r => setTimeout(r, 2000));
  ...
  ..
}

x();
```


```
let x
x -> undefined
```



---

```js
const onj2 = {
  n: 'A',
  cN: (_n) => {
    this.n = _n; // WHAT IS THIS ??
    // --OR--
    n = _n; // WHAT IS n ??
  },
};
```

```js
const abc = {
  n: 'a',
  arr: null,
  normal: function() {
    this.arr = () => { console.log(this.n) }; // now arr knows that this is abc
  },
};
```
