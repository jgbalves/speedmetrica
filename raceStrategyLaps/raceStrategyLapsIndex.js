//alert("it works!");


function addStints() {
    var table = document.getElementById('raceStrategyTable');
    var rows = parseInt(document.getElementById('stintsNumber').value);
    for (var i = 1; i <= rows; i++) {
        var tr = document.createElement('tr');
        var cell1 = document.createElement('td');
        var cell2 = document.createElement('td');
        var cell3 = document.createElement('td');
        var cell4 = document.createElement('td');
        var cell5 = document.createElement('td');
        var input2 = document.createElement('input');
        var input3 = document.createElement('input');
        var input4 = document.createElement('input');
        var input5 = document.createElement('input');
        input2.type = "number";
        input3.type = "number";
        input4.type = "number";
        input5.type = "number";
        cell1.innerHTML = i.toString();
        cell2.appendChild(input2); 
        cell3.appendChild(input3);
        cell4.appendChild(input4);
        cell5.appendChild(input5);
        tr.appendChild(cell1);
        tr.appendChild(cell2);
        tr.appendChild(cell3);
        tr.appendChild(cell4);
        tr.appendChild(cell5);
        table.appendChild(tr);        

    }

}
