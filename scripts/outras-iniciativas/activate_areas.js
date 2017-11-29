function mouseOver(stateid){
    var habilitados = $habilitados_dict;
    if(habilitados.hasOwnProperty(stateid)){
        document.getElementById(stateid).style.fill = '#606060';
    }
}

function mouseOut(stateid){
    var habilitados = $habilitados_dict;
    if(habilitados.hasOwnProperty(stateid)){
        document.getElementById(stateid).style.fill = '#909090';
    }
}
