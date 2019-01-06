var i = 0;
var HC = 0;
var HP = 0;
var WE = 0;
var inst = [0,0,0,0,0,0,0,0,0,0]

function setup() {
  loadJSON("out.json",realTime);
  drawGraph();
  setTimeout(setup, 5000)
}

function realTime(data) {
  //document.write(data.inst);
    for(var q = 0; q < 9; q++){
        inst[q] = inst[q+1]
    }
    inst[9] = parseInt(data.PAPP);
    var instColor = "black";
    var tarif = data.HHPHC;
    var tarifColor = "black";
    var maxDay = data.IMAX;
    

    if(tarif == "A") {
        tarif = "HP";
        tarifColor = "red";
    }
    if(tarif == "B") {
        tarif = "HC";
        tarifColor = "green";
    }
    if(tarif == "C") {
        tarif = "WE";
        tarifColor = "blue";
    }

    if(inst[9] > 6000*0.8) instColor = "red";

    document.getElementById("dataInst").innerHTML = "Conso : <span class = \"" + instColor + "\">" + inst[9] + " </span>W </br> Tarif : <span class = \""+tarifColor+"\">" + tarif + "</span></br> Max Jour : " + maxDay + " A";

    document.getElementById("dataPlus").innerHTML = "Cumulé : "+ data.BASE/1000 +" kWh </br> ADCO : "+data.ADCO+" </br> I inst : "+data.IINST+" A </br> Tarif : "+ data.PTEC;

}

function drawGraph() {
    //data test
    var years = [-45,-40,-35,-30,-25,-20,-15,-10,-5,0]; //x
    var africa = [0,0,0,0,0,0,0,0,0,inst]; //y
    //draw
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
            data: africa
          }
        ]
      },
        options: {
          scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
        }
    });

}

