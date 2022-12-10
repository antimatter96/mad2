Vue.component('my-tag', {
  props: ['size'], // comes from parent
  data: function () {
    return {};
  },
  computed: {
    link: function () {
      let x = this.size ?? 100; // Exists or set
      return `https://via.placeholder.com/${x}`;
    }
  },
  // Need to specify ':src="link"' instead of 'src="link"' => in prop or data or computed
  template: `
    <div>
      <img :src="link"> 
      <slot></slot>
    </div>
  `
});


var app = new Vue({ // root element
  el: "#app",
  data: {
    message: "init",
    password: "",
    combined: "",
    extra: {
      f: [1,3,4]
    }
  },
  methods: {
    resetMessage: function () {
      this.message = "init";
    }
  },
  computed: {
    validPassword: function () {
      let valid = true;
      valid = valid && this.password.length > 10

      return {
        valid: valid,
        invalid: !valid
      }
    },
    pwdLength: function () {
      // this.combined = this.message + this.password; WIll force call on change of messafge and passeord
      return `${10 + this.password.length}px`;
    },
    fullName: {
      get: function () {
        //...
      },
      set: function (newVal) {
        //...
      },
      // app.fullName = "aa"
    }
  },
  watch: { // similar to computed but
    // this gets called everyime value changes
    // caching is difficult
    // PREFER computed => declarative, cacheable
    message: function (newVal, oldVal) {
      console.log("watch.message", oldVal, "=>", newVal);
    }
  }
});


// Declarative rendering : What instead of How


/**
Reactivity : auto update in case of data change
Binding between model(data) and view(display)

Updates -> may be multiple based on just params [logged in]

 */

/**
Server  => send HTML full

Server  => sends Partial HTML [with JS], responds to endpoints

 */


/**
v-bind : ONE WAY [update variables / models => reflect on screen]

v-model : TWO WAY [mostly form data]


v-on: [event binigng]

 */

/**
class binding

give object: {
  'class1' : true/false,
  'class2' : true/false,
}

 */

/**

v-if="argument" : in DOM or not

v-show="param" : display=none or not

---

v-for="item in list"
v-for="value in object"
v-for="(value, key_name) in object"
v-for="(value, name, index) in object"

 */

/**
Loop Keys

> Need to keep track of individual elements
> For diff/ what to update 

> How to key track ? => give key to each loop element
> Update item with some key => only update that key 

 */

/*
ViewModel =>
  Derived from Model
  -> Computed Properties / Extra Fields that are not stored

Bind to View
*/

/**
Data => Instance Data of
*/


/**
MVC vs MVVM

Not comparable as such
*/


/**
Computed
-> Auto Update
-> Cached based on reactive depedencies [automatically]
*/


/**
=================
COMPONENTS

Reuseable

Same
  Structure
  Format
  OR Repeated

Mainly for readabilty and maintainabilty


-- Strucyre

Properties
  => Passed down from parent => to customize each instance


Data
  => indivdial data of this instanvce
  => Also its own watchers/computed etc


Tempaltes
  => How to render
  => Render functions also possible
  => Slots


  {{}}

  will not inerploarte text into tags
  will give errors on unclosed tags


  Also possible to use JSX

  Slot :

*/



// Object.defineProperty()  => (obj, prop, { value:x, writeble: false })


const data = {
  count: 10,
};

const newData = {}
Object.defineProperty(newData, 'count', {
  get: function () { return data.count },
  set: function (newVal) { data.count = newVal },
});

const newData2 = {}
function track() { console.log("track was called") }
function trigger() { console.log("trigger was called") }

Object.defineProperty(newData2, 'count', {
  get: function () { track(); return data.count },
  set: function (newVal) { data.count = newVal; trigger() },
});


// console.log(newData.count) => 10
// newData.count = 123 // updated data.count

// Can ALSO use proxy


// Which of the following is/are true regarding ref attribute in Vue?
//    It allows us to directly reference the DOM element
//    Ref can be accessed only after the element is mounted.

//--

// If v-if and v-for is used on the same element is used on the same element
// which of the following is true?
// 
//    v-for is evaluated first.


//--

// Which of the following is/are true regarding computed properties?
// 
//    Computed properties are by default getter only.
//    A Computed property should not be directly mutated.


//---
let c = new Vue({ el: "#app3", data: { message: "C" } });
let b = new Vue({ el: "#app2", data: { message: "B" } });
let a = new Vue({ el: "#app1", data: { message: "A" } });

