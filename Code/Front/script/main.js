function setup() {
  loadJSON("../Script/state.json",realTime);
  setTimeout(setup, 5000)
}

function realTime(data) {
  //document.write(data.inst);
    var inst = data.inst;
    var instColor = "black";
    var tarif = data.tarif;
    var tarifColor = "black";
    var maxDay = data.maxDay;

    if(tarif == "HP") tarifColor = "red";
    if(tarif == "HC") tarifColor = "green";
    if(tarif == "WE") tarifColor = "blue";

    if(inst > data.maxP*0.8) instColor = "red";

    document.getElementById("dataInst").innerHTML = "Conso : <span class = \"" + instColor + "\">" + inst + " </span>W </br> Tarif : <span class = \""+tarifColor+"\">" + tarif + "</span></br> Max Jour : " + maxDay + " W";
}

