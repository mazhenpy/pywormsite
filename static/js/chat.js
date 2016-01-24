var socket;
    if (!window.WebSocket) {
        window.WebSocket = window.MozWebSocket;
    }
    // Javascript Websocket Client
    if (window.WebSocket) {
        socket = new WebSocket("ws://www.pyworm.com:8000/websocket");
        socket.onmessage = function (event) {
            if(event.data){
                var attr = $("#attr").html();
                var newmessage = "<div class=\"msg\">"+"<span>"+ attr + "：" + event.data+"</span>"  + "</div>";
                $(".form-control").append(newmessage);
                var div = document.getElementById('responseText');
                div.scrollTop = 9999;
                }
        };
        socket.onopen = function (event) {
            var status = '<span>已与服务器建立连接</span>';
            $("#status").html(status);
//            var ta = document.getElementById('status');
//            ta.value = "已与服务器建立连接";
        };
        socket.onclose = function (event) {
            var status = '<span>已与服务器断开连接</span>';
            $("#status").html(status);
        };
    }
    // Send Websocket data
    function send(message) {
        $("#msg").val('');
        if (!window.WebSocket) {
            return;
        }
        if (socket.readyState == WebSocket.OPEN) {
            socket.send(message);
        }
    }


function add() {
    var div = $(".msg");
    div.scrollTop = div.scrollHeight;
}


$(document).ready(function(){
        $("#msg").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            $("#msg").click();
                send(this.form.message.value)
        }
  });
});
