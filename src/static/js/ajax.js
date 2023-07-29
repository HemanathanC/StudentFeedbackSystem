function index(value)
{
    $.ajax({
        type:'POST',
        url:'/index_ajax',
        data:{value:value},
        success:function(response)
        {
            document.getElementById('include').innerHTML=response;
            feed();
        }
    });
}
function validate_login()
{
    $.ajax({
        type:'POST',
        url:'/validate_admin',
        data:{},
        success:function(response)
        {
            document.getElementById('include').innerHTML=response;
        }
    });
}
function New()
{
    $.ajax({
        type:'POST',
        url:'/New',
        data:{},
        success:function(response)
        {
            window.location.href=response;
        }
    });
}
function overall()
{
    $.ajax({
        type:'POST',
        url:'/overall',
        data:{fac:document.getElementById('fac').innerText,
              sub:document.getElementById('sub').innerText,
              year:document.getElementById('year').value},
        success:function(response)
        {
            document.getElementById('overall').remove();
            document.getElementById('ajax').innerHTML=response;
        }
    });
}
function logout()
{
    if(confirm('Are you sure you want to logout?'))
    {
        alertify.set('notifier','position','top-center');
        alertify.notify('You are logging out...', 'success', 2, function(){
            window.location.href='/';
        });
    }
}