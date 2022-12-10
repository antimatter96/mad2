const obj = {
  x: 1,
  y: 1,

  set nums(xxx) {
    xxx = xxx.split(',');
    this.x = xxx[0];
    this.y = xxx[1];
  },

  get nums() {
    return this.x + ',' + this.y;
  },

  pow: function() {
    let r = 1;
    for (let i = 1; i < this.y; i++) {
      r = r * this.x;
    }

    return r;
  },

};
obj.nums = '2,3';
console.log(obj.pow());


const ePowX = {
  x: 1,
  n: 1,

  set nums(xxx) {
    xxx = xxx.split(',');
    this.x = xxx[0];
    this.n = xxx[1];
  },

  get fx() {
    let r = 1;
    let y = 1;
    for(let i = 1; i < this.n; i++) {
      y = y * this.x;
      console.log(y);
      r = r + y;
    }
    return r;
  },

};
ePowX.nums = '2,3';
console.log(ePowX.fx);


const s = {
  n: 'Name 1',
  c: 'Code',
};

const course = {
  __proto__: s,
  n: 'Name',
  c: 'Code',
};

const stu = {
  __proto__: course,
  sN: 'Stu Name',
  sC: 'Stu City',
};

const { c } = stu;
console.log(c);

console.log(Object.keys(stu), Object.entries(stu));
console.log(stu.n);
console.log(stu.c);

