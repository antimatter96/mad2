setTimeout(() => {
  console.log('st A');
}, 0);
console.log('main A');
setTimeout(() => {
  console.log('st B');
}, 0);
console.log('main B');


let x = (n) => {
  let l = n.split('').reverse();


  let st = Date.now();
  let hand = setInterval(() => {
    console.log(Date.now() - st, l.pop());
  }, 1000)

  setTimeout(() => {
    clearInterval(hand)
  }, (n.length + 1) * 1000);
};

x('ABCD');
