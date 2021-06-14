function button_click(btn){
    var count = 1;
    var property = document.getElementById(btn);
    if (count == 0) {
        property.style.backgroundColor = "#FFFFFF"
        //.className = "btn btn-danger text-white";
        //style.backgroundColor = "#FFFFFF"
        count = 1;        
    }
    else {
        property.style.backgroundColor = "#FFFFFF"
        //.className = "btn btn-success text-white";
        //style.backgroundColor = "#7FFF00"
        count = 0;
    }

}
