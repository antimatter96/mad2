Vue.component('my-tag', {
  props: ['size'], // comes from parent
  data: function () { // MUST BE A FUNCTION
    return {
      count: 0,
    };
  },
  methods: {
    inc: function () {
      this.count++;
      // this.size += 50; //WARNING
      this.$emit("tell-parent", [Math.random() * 100])
    }
  },
  computed: {
    newSize: function() {
      return  parseInt(this.size, 10) + (this.count * 50);
    }
  },
  template: `
    <div>
      <p>{{count}} | {{size}} | {{newSize}}</p>
      <button v-bind:style="{fontWeight: newSize}" v-on:click="inc">INC</button>
      <hr>
    </div>
  `
});


var app = new Vue({ // root element
  el: "#app",
  data: function () {
    return {
      combined: 0,
    }
  },
  methods: {
    incrementCount: function (x) {
      console.log('they said', x);
      this.combined++;
    }
  },
});

//
// v-html= “text” 
