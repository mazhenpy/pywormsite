function a(id) {
    var words = id.split(",");
    var blog_id = words[0];
    var p_id = words[1];
    var k=1;
    //alert(blog_id,p_id);
    $("#user_content00"+p_id).submit(function () {
        if(k){
            var content = $("#id_content00"+p_id).val();
            //alert(content);
            if (content.length == 0)
                {
                return false;
                }
            else{
                $.ajax({
                    type: "post",
                    dataType: "json",
                    url: "/blog/" + blog_id + "/",
                    data: {
                        'content': content,
                        'p_id': p_id
                    },

                    success: function (data){
                        window.location.reload();

                    }
                });
                }
        k=0;
        return false}
    });
    }

