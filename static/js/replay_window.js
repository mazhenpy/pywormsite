function b(id){
        $('.theme-popover-mask-replay0'+id).fadeIn(100);
        $('.theme-popover-replay0'+id).slideDown(200);
    }


jQuery(document).ready(function($) {
    $('.theme-poptit-replay .close').click(function(){
        $('.theme-popover-mask-replay').fadeOut(100);
        $('.theme-popover-replay').slideUp(200);
    })
});