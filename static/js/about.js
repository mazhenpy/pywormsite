function b() {
    var k = 1;
    $("#msg_form").submit(function () {
        if (k) {
            var content = $("#msg_content").val();
            //alert(content);
            if (content.length == 0) {
                return false;
            }
            else {
                $.ajax({
                    type: "post",
                    dataType: "json",
                    url: "/about/",
                    data: {
                        'content': content
                    },

                    success: function (data) {
                        var status = data.status;
                        if(status == 'fail'){
                            $("#msg_content").val('');
                        }
                        else{
                            $("#msg_content").val('');
                            var msg ="<div class=\"user_replay\">"+
                                        "<div class=\"replay replay_user\"><small>"+data.key+"</small></div>"+
                                        "<br>"+
                                        "<div class=\"replay replay_time\"><small>"+data.value+"</small></div>"+
                                    "</div>";
                            $(".con").append(msg);
                        }

                    }
                });
            }
            k = 0;
            return false
        }
    });
}
