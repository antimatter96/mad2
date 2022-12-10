import { divStyle1, divStyle2 } from './m2.js';



setTimeout(() => {
  divStyle1.width = "50px";
  const div1Style = document.getElementById('id1').style;
  div1Style.backgroundColor = divStyle1.color;
  div1Style.width = divStyle1.width;
  div1Style.height = divStyle2.height;
}, 0);

