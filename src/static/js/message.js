$(document).ready(function(){
    const msg = $("input[type='hidden']").val();
    if(msg==1){
        window.onload = function() 
        { 
            $.ajax({
                type: 'POST',
                url: '/index_ajax',
                data: {value:'admin'},
                success: function (response) 
                {
                    document.getElementById("include").innerHTML=response; 
                }
            });
        };
    }
    else if(msg==2){
        window.onload = function() 
        { 
            $.ajax({
                type: 'POST',
                url: '/index_ajax',
                data: {value:'dc'},
                success: function (response) 
                {
                    document.getElementById("include").innerHTML=response; 
                }
            });
        };
    }
    else{
        window.onload = function() 
        { 
            $.ajax({
                type: 'POST',
                url: '/index_ajax',
                data: {value:'feedback'},
                success: function (response) 
                {
                    document.getElementById("include").innerHTML=response;
                    feed();
                }
            });
        };
    }
    if(msg){
        alertify.set('notifier','position','top-center');
        alertify.error('Invalid Username/Password!');
    }
});