const newC = {
  props: ['name'], // comes from parent
  data: function () {
    return {
      currentUser: {
        name: "ARRRRTTTTTTTTT"
      }
    };
  },
  template: `
    <div>
      <slot name="header" :user="currentUser">HEADER SLOT KA DEFAULT CONTENT AGAR KUCH NAHI DIYA</slot>

      <br>
      <br>
      <slot name="slot_name_1"> agar slot_name_1 nahi diya to kya aaega </slot>


      <br>
      <br>
      <slot name="slot_name_2" :key_1="'value 1'" :key_2="'value 2'"> agar slot_name_2 nahi diya to kya aaega </slot>
      <br>
      <br>
      <br>
      <slot name="slot_name_3"> agar slot_name_3 nahi diya to kya aaega </slot>
      <br>
      <br>
      <br>
      EVERYTHING OUTSIDE THE TEMPLAGE TAG
      <br>
      <slot> EK DEFALT [agar sab kuch kisi named slot me he ]</slot>
    </div>
  `
};


var app = new Vue({ // root element
  el: "#app",
  components: {
    'something': newC
  },
});
