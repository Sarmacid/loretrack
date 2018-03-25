function init_encounter_creator(){
    document.getElementById("content").innerHTML = `
        <p></p>
        <h3>Choose characters:</h3>
        <div id="characters_div">
        </div>
        </br>
        <h3>Choose monsters:</h3>
        <div name="MonsterPicker" style="width: 25%;">
            <select id="select-monster-empty" data-placeholder="Select a monster to add...">
            <option value="">None</option>
            </select>
        </div>
        </br>
        <div name="monsters" id="monsters" style="width: 25%;">
        </div>
        <div name="encounter_details" style="width: 25%;">
            <h3>Name encounter:</h3>
            <input id="encounter_name" type="text" class="form-control" name="name" placeholder="Courtyard fight" value="" autocomplete="off" required>
        </div>
        </br>
        </br>
        <button class="btn btn-primary" id="save">Save encounter</button>
    `;

    function get_selected_characters() {
        var inputs = document.getElementById('characters_div').getElementsByTagName('input');
        var characters = [];
        for (i = 0; i < inputs.length; i++) {
            if (inputs[i].checked) {
                characters.push(inputs[i].value);
            }
        }
        return characters;
    }

    function get_selected_monsters() {
        var inputs = document.getElementById('monsters').getElementsByTagName('input');
        var monsters = [];
        for (i = 0; i < inputs.length; i++) {
            if (Number(inputs[i].value) > 0){
                var dict = {};
                dict['m_id'] = inputs[i].id;
                dict['amount'] = inputs[i].value;
                monsters.push({'m_id': inputs[i].id, 'amount': inputs[i].value});
            }
        }
        return monsters;
    }

    function get_characters(handleData) {
        var c_id = get_campaign_id();
        var data = {c_id: c_id};
        var characters = null;

        $.ajax({
            url: "/character/api/v1.0/get_all",
            type: "POST",
            dataType: "json",
            global: false,
            contentType: 'application/json',
            success: function (msg) {
                handleData(msg.Data);
            },
            error: function(msg) {
                my_alert(msg.responseJSON.Response, 'red', 'Oh no!');
            },
            data: JSON.stringify(data)
        });
    };

    function add_monster(monster) {
        if (monster == null || document.getElementById(monster.m_id)) {
            return;
        }

        var pre_input_div = document.createElement("DIV");
        pre_input_div.className = "input-group-prepend";

        var textnode = document.createTextNode(monster.name);

        var post_input_div = document.createElement("DIV");
        post_input_div.className = "input-group-append";

        var minus_button = document.createElement("BUTTON")
        minus_button.className  = "btn btn-outline-secondary";
        minus_button.innerHTML = "-";
        minus_button.name = "minus";
        minus_button.setAttribute( "onClick", "change_value(this, 'substract'); return false;" );
        pre_input_div.appendChild(minus_button);

        var amount = document.createElement("INPUT")
        amount.className  = "form-control";
        amount.maxlength = "3";
        amount.value  = 0;
        amount.id = monster.m_id;

        var plus_button = document.createElement("BUTTON")
        plus_button.className  = "btn btn-outline-secondary";
        plus_button.innerHTML = "+";
        plus_button.name = "plus";
        plus_button.setAttribute( "onClick", "change_value(this, 'add'); return false;" );
        post_input_div.appendChild(plus_button);

        var newline = document.createElement("BR");

        var big_div = document.getElementById("monsters");

        var single_monster_div = document.createElement("DIV");
        single_monster_div.className = "input-group mb-3 input-group-sm";
        big_div.appendChild(single_monster_div);

        single_monster_div.appendChild(textnode);
        single_monster_div.appendChild(pre_input_div);
        single_monster_div.appendChild(amount);
        single_monster_div.appendChild(post_input_div);
        single_monster_div.appendChild(newline);
    }

    function build_character_picker() {
        get_characters(function(characters){
            var chars_div = document.getElementById('characters_div');
            for (i = 0; i < characters.length; i++) {
                var single_char_div = document.createElement("DIV");
                single_char_div.className = "custom-control custom-checkbox";
                chars_div.appendChild(single_char_div);

                var char_check = document.createElement("INPUT");
                char_check.className = "custom-control-input";
                char_check.value = characters[i].pc_id;
                char_check.type = "checkbox";
                char_check.id = "checkbox_" + characters[i].pc_id;
                single_char_div.appendChild(char_check);

                var label = document.createElement("LABEL");
                label.className = "custom-control-label";
                label.setAttribute("for", "checkbox_" + characters[i].pc_id);
                label.innerHTML = characters[i].name;
                single_char_div.appendChild(label);

                var newline = document.createElement("BR");
                single_char_div.appendChild(newline);
            }
        });
    }

    build_character_picker();

    $('#select-monster-empty').selectize({
        valueField: 'm_id',
        labelField: 'name',
        searchField: 'name',
        create: false,
        persist: false,
        options: [],
        preload: true,
        allowEmptyOption: false,
        load: function(query, callback) {
            $.ajax({
                url: "/monster/api/v1.0/get_all",
                type: 'GET',
                dataType: "json",
                error: function() {
                    callback();
                },
                success: function (res) {
                    callback(res.Data);
                }
            });
        },
        onChange: function(value) {
            var monster = $(this)[0].options[value];
            add_monster(monster);
        }
    });

    $('#save').click(function(event) {
        event.preventDefault();
        var characters = get_selected_characters();
        var monsters = get_selected_monsters();
        var c_id = get_campaign_id();
        var name = document.getElementById('encounter_name').value;
        var data = {
            pc_ids: characters,
            monsters: monsters,
            c_id: c_id,
            name: name
        }

        $.ajax({
            url: "/encounter/api/v1.0/save",
            type: "POST",
            dataType: "json",
            contentType: 'application/json',
            success: function (msg) {
                my_alert(msg.Response, 'green');
            },
            error: function(msg) {
                my_alert(msg.responseJSON.Response, 'red', 'Oh no!');
            },
            data: JSON.stringify(data)
        });
        event.preventDefault();
    });
}

function change_value(button, operation) {
    if (operation == 'add'){
        var input = $(button).parent().prev('input')[0];
        var new_value = Number(input.value);
        new_value = new_value + 1;
    }else if(operation == 'substract'){
        var input = $(button).parent().next('input')[0];
        var new_value = Number(input.value);
        new_value = new_value - 1;
    }
    if (new_value >= 0) {
        input.value = new_value;
    }
}
