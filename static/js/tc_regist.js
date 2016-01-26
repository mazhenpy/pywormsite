$(function(){

     $("#put2").click(function(){

        username=$("#id_usernm").val();
		password=$("#id_passwd").val();
        password2=$("#id_passwd2").val();
        $.ajax({
        type:"POST",
        url:"/ajax_regist/",
        data:{'username':username,'password':password,'password2':password2},
        dataType:"text",
        success: function(data) {
		if(data){
			$("#regist_error").html(data)
}
		else{
			$.ajax({
				type:"POST",
        		url:"/regist/",
				data:{'username':username,'password':password},
				success: function() {
                    $('.theme-popover-mask-regist').fadeOut(100);
                    $('.theme-popover-regist').slideUp(200);
                    $('.theme-popover-mask-alert').fadeIn(100);
                    $('.theme-popover-alert').slideDown(200);

}
})
			
}
          	  	
        }
	
      });

     })

  });