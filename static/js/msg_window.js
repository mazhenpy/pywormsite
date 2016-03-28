function a(){
        $("#msg_content").val('');
        $('.theme-popover-mask-msg').fadeIn(100);
        $('.theme-popover-msg').slideDown(200);
    }

jQuery(document).ready(function($) {
    $('.theme-poptit-msg .close').click(function(){
        $('.theme-popover-mask-msg').fadeOut(100);
        $('.theme-popover-msg').slideUp(200);
    })
});


