$(function(){
     $("#put1").click(function(){
        username=$("#id_usernm_login").val();
		password=$("#id_passwd_login").val();
        $.ajax({
        type:"POST",
        url:"/ajax_login/",
        data:{'username':username,'password':password},
        dataType:"text",
        success: function(data) {
		if(data){
			$("#login_error").html(data)
        }
		else{
			$.ajax({
			    type:"POST",
        		url:"/index/",
			    data:{'username':username,'password':password},
			success: function(data) {
//		 	    location.reload()
                window.location.href="/admin/";
            }
            })
            }
        }
      });
     })
  });

  