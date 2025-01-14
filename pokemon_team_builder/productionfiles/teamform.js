document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[id^="id_pokemon"]').forEach(select => {
        var pokemonId = parseInt(select.value);
        var wholeid = String(select.id);
        var idint = wholeid[wholeid.length - 1];
        populateAbilitiesAndMoves(pokemonId, idint);
        })
    document.querySelectorAll('[id^="id_pokemon"]').forEach(select => {
        select.addEventListener('change', function() {
            var pokemonId = parseInt(this.value);
            var wholeid = String(this.id);
            var idint = wholeid[wholeid.length - 1];
            populateAbilitiesAndMoves(pokemonId, idint);
        })
    })
    function populateAbilitiesAndMoves(pokemonId, idint) {
        var abilityFieldId = 'id_ability' + idint;
            var moveFieldBaseId = 'id_move' + idint + '_';

            // AJAX request to fetch data for the selected Pokémon from get pokemon data view
            fetch('/get_pokemon_data/' + pokemonId + '/')
            .then(response => response.json())
            .then(data => {
                var abilities = data.pokemon_data.abilities;
                var moves = data.pokemon_data.moves;

                // Populate the abilities dropdown
                var abilityField = document.getElementById(abilityFieldId);
                abilityField.innerHTML = "";
                abilities.forEach(function(ability) {
                    var option = document.createElement('option');
                    option.value = ability.id;
                    option.text = ability.name;
                    abilityField.appendChild(option);
                });

                // Populate the moves dropdowns
                for (var i = 1; i <= 4; i++) {
                    var moveFieldId = moveFieldBaseId + i;
                    var moveField = document.getElementById(moveFieldId);
                    moveField.innerHTML = "";
                    moves.forEach(function(move) {
                        var option = document.createElement('option');
                        option.value = move.id;
                        option.text = move.name;
                        moveField.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error fetching pokemon data', error));
        }
    });
