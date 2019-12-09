var divs = document.getElementsByClassName("subContent");
window.onload = function(){toggleOnOff();toggleOnOff();};

function toggleOnOff(){
    var wifi_togle = document.getElementById("wifiTogggle");
    var mode = document.getElementsByName("is_offline_mode");
    var status = document.getElementsByName("wifiStatus");
    var network_setting = document.querySelector("div.network_setting");
    if(wifi_togle.checked == true){
        network_setting.style.display = "block";
        // status[0].innerHTML = "Offline mode: no";
        mode[0].value = "Online";
    }else{
        network_setting.style.display = "none";
        // status[0].innerHTML = "Offline mode: yes";
        mode[0].value = "Offline";
    }
    foldEverything();
};



