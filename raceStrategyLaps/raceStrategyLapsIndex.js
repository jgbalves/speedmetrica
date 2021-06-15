//Gives Drivers names
var drivers = ["Ninja", 'Letas', 'Jalves'];

//Gives tire sets
var tyreSets = ["Set 1", 'Set 2', 'Set 3'];

//Add stints to Race Strategy table
$('#stintsAdder').click(function() {
    let table = $('#raceStrategyTable');
    let rowNum = parseInt($('#stintsNumber').val(), 10);
    let resultHtml = ["<tr>",
                    '<th colspan="5">Race Strategy</th>',
                    "</tr>",
                    '<tr>',
                    '<th>Stints</th>',
                    '<th>Lap In</th>',
                    '<th>Fuel added</th>',
                    '<th>Driver</th>',
                    '<th>Tyre Set</th>',
                    '</tr>'
    ]

    for (let i = 0; i < rowNum; i++){
        resultHtml += [
            "<tr>",
            "<td>",
            ("Stint " + parseInt(i + 1, 10)),
            "</td>",
            '<td><input type="number"></td>',
            '<td><input type="number"></td>',
            '<td>',
            '<select name="Driver" id="">',
                '<option value="Ninja">Ninja</option>',
                '<option value="Letas">Letas</option>',
                '<option value="Jalves">Jalves</option>',
            '</select>',
            '</td>',
            '<td><select name="Set" id="tyreSetSelect"></select></td>',
            '</tr>'
        ].join("\n");
    }
    table.html(resultHtml);
        return false;
}
);

/*
$.each(tyreSets, function(key, value) {
    $('#tyreSetSelect').append($('<option>', {value: key}).text(value));
}
);
*/

$.each(tyreSets, function(key, value) {
    $('#tyreSetSelect')
         .append($('<option>', { value : key })
         .text(value));
});