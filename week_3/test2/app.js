var app = new Vue({ // root element
  el: "#app",
  data: {
    message: "Hello World",
    count: 0,
    vistorName: '',
    visitors: [],
    dark: false,
    styleObject: {
      color: 'red',
      fontSize: '13px'
    }
  },
  methods: {
    sayHi: function () {
      this.message = "Hi"; // ERROR
      // this.data.message = "Hi"; // ERROR

      this.count++

      this.visitors.push(this.vistorName)
      this.vistorName = "";


    },
    toggleTheme: function () {
      this.dark = !this.dark;
    }
  },
  computed: {
    count_2: function () {
      return this.visitors.length;
    },
    styleObject: () => ({ // Will log  error as also in data
      color: 'red',
      fontSize: '13px'
    }),
    // styleObject3: () => ({ DOES not work
    //   color: this.dark ? "red" : "green",
    //   fontSize: '13px'
    // }),
    styleObject3: () => { //DOES not work
      console.log(this); // ???? Not app
      return {
      color: this.dark ? "red" : "green",
      fontSize: '13px'
    }},


    styleObject2: function () { // Will log  error as also in data
      return {
        color: this.dark ? "red" : "green",
        fontSize: '13px',
      }
    }
  }
})

// app.other = "jk" //  WARN : other not accessbile
// app.data.other = "jk" //  WARN : other not accessbile



/**
 * 
 * v-on:click=”toggleSeen”
 * @click=”toggleSeen”
 */
