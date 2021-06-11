//Gives Drivers names
var drivers = ["Ninja", 'Letas', 'Jalves'];

//Gives tire sets
var tyreSets = ["Set 1", 'Set 2', 'Set 3'];

//Add stints to Race Strategy table
$('#stintsAdder').click(function() {
    let table = $('#raceStrategyTable');
    let rowNum = parseInt($('#stintsNumber').val(), 10);
    let resultHtml = '';

    for (let i = 0; i < rowNum; i++){
        resultHtml += [
            "<tr>",
            "<td>",
            ("Stint " + i+ parseInt(1, 10)),
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