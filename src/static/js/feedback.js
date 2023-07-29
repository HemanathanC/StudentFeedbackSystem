function feed() {
    const data = document.querySelectorAll('#sub');
    const cond = document.querySelectorAll('#cond');
    let sub = document.getElementById('subjects');
    let thead = document.querySelector('thead');
    let tr = document.querySelectorAll('tr');

    for(var i=0;i<data.length;i++){
     //Adding checkboxes   
        const div = document.createElement('div');
        div.setAttribute('class','form-check');
        
        const chx = document.createElement('input');
        chx.setAttribute('type','checkbox');
        chx.setAttribute('class','form-check-input')
        chx.setAttribute('name','subjects');
        chx.setAttribute('value',data[i].value);
        chx.setAttribute('id',data[i].value);
        if(cond[i].value=='no')
        {   
            chx.setAttribute('checked',true);
            chx.setAttribute('disabled',true);
        }
        div.appendChild(chx);

        const lbl = document.createElement('label');
        lbl.setAttribute('class','form-check-label');
        lbl.setAttribute('for',data[i].value);
        lbl.appendChild(document.createTextNode(data[i].value));
        div.appendChild(lbl);

        sub.appendChild(div);

    //Adding thead subject names
        const th = document.createElement('th');
        th.appendChild(document.createTextNode(data[i].value));
        thead.children[0].appendChild(th);
    
    //Adding select boxes
        for(var k=1;k<tr.length;k++){
            const td = document.createElement('td');
            const select = document.createElement('select');
            select.setAttribute('class',data[i]); 
            select.classList.add('form-select');   
            select.setAttribute('disabled',true);
            for(var j=1;j<=5;j++){
                const option = document.createElement('option');
                option.value = j;
                option.text = j;
                select.appendChild(option);
            }
            td.appendChild(select);
            tr[k].appendChild(td);
        }
    }
    change();
}
function change(){
    let checkboxes = document.querySelectorAll("input[name='subjects']");
    let tr1 = document.querySelectorAll('tr');
    for(var i=1;i<tr1.length;i++){
        for(var j=0;j<checkboxes.length;j++){
            if(checkboxes[j].checked)
                tr1[i].children[j+1].firstElementChild.removeAttribute('disabled');
            else
                tr1[i].children[j+1].firstElementChild.setAttribute('disabled',true);
        } 
    }
}
function validate(){
    const data = document.querySelectorAll('#sub');
    let values = {}
    for(var s=0;s<data.length;s++){
        let q1 = document.getElementsByClassName(data[s]);
        var val = [];
        for(var a=0;a<q1.length;a++){
            if(!(q1[a].disabled)){
                val.push(q1[a].value);
            }
        }
        if(val.length != 0)
            values[data[s].value] = val;
    }
    $.ajax({
        type:'POST',
        url:'/validate_feedback',
        contentType: "application/json",
        data: JSON.stringify(values),
        success:function(response)
        {
            document.getElementById('include').innerHTML = response;
        }
    }); 
}