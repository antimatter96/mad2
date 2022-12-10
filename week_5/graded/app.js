
const a = fetch("app.html")

a.then(r => {
  if (!r.ok) {
    throw new Error(r.status);
  }
  return r.text();
}).then(d => {
  console.log("DATA", d)
}).catch(e => {
  console.log(e, "<<")
})


async function funcl() {
  new Promise(rej => setTimeout(rej, 4000));
  async function func2() {
    await new Promise(rej => setTimeout(rej, 2000));
    console.log("Finished", new Date());
  }
  func2();
}
console.log(new Date())
funcl();


let start = 5;
function check() {
  return new Promise((res, rej) => {
    let a1 = setInterval(() => {
      start++;
      if (start === 7) {
        console.log("Reached");
        clearInterval(a1);
        res("{ass")
        rej("Fail");
      }
      else {
        console.log("Yet to Reach");
      }
    }, 500);
  })
}

check().then(
  pass => console.log(pass)
).catch(
  fail => console.log(fail)
);

//----------

let x = 2,
  n = 3,
  k = 2;

const Promise1 = new Promise((resolved, rejected) => {
  if (k < n) {
    resolved(x);
  } else {
    rejected('Bad Promise');
  }
});


const promise2 = Promise1.then((x) => {
  return x * x * x
});

promise2
  .then((x) => {
    console.log("pass>>", x)
  })
  .catch((err) => {
    console.log(">>>>>", err)
  })
