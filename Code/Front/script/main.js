var i = 0;
var HC = 0;
var HP = 0;
var WE = 0;

function setup() {
  loadJSON("../Script/state.json",realTime);
  if (i == 0) drawGraph();
  i ++;
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

    HC = data.HC;
    HP = data.HP;
    WE = data.WE;
}

function drawGraph() {
    //data test
    var years = [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050]; //x
    var africa = [86,114,106,106,107,111,133,221,783,2478]; //y
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

    var data1 = {
        labels: ["match1", "match2", "match3", "match4", "match5"],
        datasets: [
            {
                label: "TeamA Score",
                data: [10, 50, 25, 70, 40],
                backgroundColor: [
                    "#DEB887",
                    "#A9A9A9",
                    "#DC143C",
                    "#F4A460",
                    "#2E8B57"
                ],
                borderColor: [
                    "#CDA776",
                    "#989898",
                    "#CB252B",
                    "#E39371",
                    "#1D7A46"
                ],
                borderWidth: [1, 1, 1, 1, 1]
            }
        ]
    };

    var options = {
        responsive: true,
        title: {
            display: true,
            position: "top",
            text: "Doughnut Chart",
            fontSize: 18,
            fontColor: "#111"
        },
        legend: {
            display: true,
            position: "bottom",
            labels: {
                fontColor: "#333",
                fontSize: 16
            }
        }
    };

    var ctxHCHP = document.getElementById("HPHC");
    var myDoughnutChart = new Chart(ctxHCHP, {
    type: 'doughnut',
    data: data1,
    options: options
});

}

