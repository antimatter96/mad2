const newC = {
  props: [],
  data: function () {
    return {};
  },
  template: `
    <h1>New Componenet</h1>
  `
};


var app = new Vue({ // root element
  el: "#app",
  components: {
    'something': newC
  },
});

