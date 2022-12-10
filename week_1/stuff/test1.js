const obj = {
  n: 'A',
  cN: function(n) {
    this.n = n;
  },
};
console.log(obj);
obj.cN('B');
console.log(obj);


const x = {name: 'rohit'};
x.name = 'Mohit';

console.log(x);


const onj2 = {
  n: 'A',
  cN: (_n) => {
    n = _n;
  },
  cNN: () => {
    console.log(this.n);
  },
};
console.log(onj2);
onj2.cN('B');
console.log(onj2);
onj2.cNN();

const abc = {
  n: 'a',
  arr: null,
  normal: function() {
    this.arr = () => {
      console.log(this.n);
    };
  },
};

console.log(abc);
abc.normal();
console.log(abc);
abc.arr();
