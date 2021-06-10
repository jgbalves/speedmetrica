//Gives Drivers names
var drivers = ["Ninja", 'Letas', 'Jalves'];

//Gives tire sets
var tyreSets = ["Set 1", 'Set 2', 'Set 3'];

//Add stints to Race Strategy table
function addStints() {
    var table = document.getElementById('raceStrategyTable');
    var rows = parseInt(document.getElementById('stintsNumber').value);
    for (var n = 1; n <= rows; n++) {
        var tr = document.createElement('tr');
        var cell1 = document.createElement('td');
        var cell2 = document.createElement('td');
        var cell3 = document.createElement('td');
        var cell4 = document.createElement('td');
        var cell5 = document.createElement('td');
        var input2 = document.createElement('input');
        var input3 = document.createElement('input');
        var input4 = document.createElement('select');
        var input5 = document.createElement('select');
        input2.type = "number";
        input3.type = "number";
        cell1.innerHTML = n.toString();
        cell2.appendChild(input2); 
        cell3.appendChild(input3);
        cell4.appendChild(input4);
        for (var i = 0; i < drivers.length; i++){
            var option = document.createElement("option");
            option.value = drivers[i];
            option.text = drivers[i];
            input4.appendChild(option);
        }
        cell5.appendChild(input5);
        for (var z = 0; z < tyreSets.length; z++){
            var option = document.createElement("option");
            option.value = tyreSets[i];
            option.text = tyreSets[i];
            input4.appendChild(option);
        }
        tr.appendChild(cell1);
        tr.appendChild(cell2);
        tr.appendChild(cell3);
        tr.appendChild(cell4);
        tr.appendChild(cell5);
        table.appendChild(tr);        

    }

}

$('#stintsAdder').click(function() {
    let table = $('#raceStrategyTable');
    let rowNum = parseInt($('StintsNumber').val(), 10);
    let resultHtml = '';

    for (let i = 0; i < rowNum; i++){
        resultHtml += [
            "<tr>",
            "<td>",
            ("Stint" + i+1),
            "</td>",
            '<td><input type="number"></td>',
            '<td><input type="number"></td>',
            '<td><input type="number"></td>',
            '<td><select name="Driver" id=""></select></td>',
            '<td><select name="Set" id=""></select></td>',
            '</tr>'
        ].join("\n");
    }
    table.html(resultHtml);
        return false;
}
);
