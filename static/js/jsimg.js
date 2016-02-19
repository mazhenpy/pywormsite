$(function(){
     $(window).load(function(){
       $.ajax({
        type:"POST",
        url:"/ajax_jsimg/",
        dataType:"text",
        success: function(data) {
          $("#p").html(data)
        }
      });
     })
  });