jQuery(document).ready(function($) {
    $('.theme-regist').click(function(){
        document.getElementById("regist_form").reset();
        $("#regist_error").empty();
        $('.theme-popover-mask-regist').fadeIn(100);
        $('.theme-popover-regist').slideDown(200);
    });
    $('.theme-poptit-regist .close').click(function(){
        $('.theme-popover-mask-regist').fadeOut(100);
        $('.theme-popover-regist').slideUp(200);
    })
});

jQuery(document).ready(function($) {
    $('.theme-login').click(function(){
        document.getElementById("login_form").reset();
        $("#login_error").empty();
        $('.theme-popover-mask-login').fadeIn(100);
        $('.theme-popover-login').slideDown(200);
    });
    $('.theme-poptit-login .close').click(function(){
        $('.theme-popover-mask-login').fadeOut(100);
        $('.theme-popover-login').slideUp(200);
    })
});

//注册成功
jQuery(document).ready(function($) {
    $('#button-alert').click(function(){
        $('.theme-popover-mask-alert').fadeOut(100);
        $('.theme-popover-alert').slideUp(200);
    });
});



//获取active状态
//window.onload = function (){
//    var id = window.location.href.substr(-2,2);
//    if(id == 'og'){
//        $('#search_blog').addClass('active');
//    }
//    else if(id == 't/'){
//        $('#about').addClass('active');
//    }
//    };

$(document).ready(function () {
    $('.navbar-nav>li').click(function (e) {
        var id =  $(this).attr("id").substr(-2,2);
        var page_id = window.location.href.substr(-2,2);
        if (page_id == id){
            e.preventDefault()
        }
    });
});

