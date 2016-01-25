$(document).ready(function(){
  $("#my_blog").click(function(){
  t = setTimeout(function(){
  $("#dh").toggle(100);
},100);
  });
  $("body").click(function(){
  $("#dh").hide();
});
});

