//分页焦点，没有分页不显示
window.onload = function (){
    if(document.getElementById("2")==undefined){
        document.getElementById('previous_page').style.display = 'none';
    }
    else{
        var id = window.location.href.substr(-1,1);
        if(id == '/'){
            $('#'+1).addClass('active');
        }
        $('#'+id).addClass('active');
        }
    };


$(document).ready(function () {
    $('.pagination li').click(function (e) {
        var id =  $(this).attr("id");
        var page_id = window.location.href.substr(-1,1);
        if (page_id == id){
            e.preventDefault()
        }
    });
});



