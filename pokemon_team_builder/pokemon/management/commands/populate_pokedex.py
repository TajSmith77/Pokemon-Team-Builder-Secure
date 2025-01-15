import logging
import requests
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon, Type, Move, Ability

class Command(BaseCommand):
    help = 'Fetches Pokemon data from PokeAPI and inserts it into the pokedex table'

    def handle(self, *args, **options):
        # Set up logging to show progress in the console
        logger = logging.getLogger('django')
        
        # Fetch Pokémon dex data from PokeAPI
        dex_response = requests.get(url="https://pokeapi.co/api/v2/pokemon/?&limit=5")
        dex_response.raise_for_status()
        dex_data = dex_response.json()

        logger.info(f"Starting to process {len(dex_data['results'])} Pokémon entries.")

        # Lists to collect bulk insert data
        bulk_pokemon = []
        bulk_abilities = []
        bulk_types = []
        bulk_moves = []

        # Loop through each Pokémon in the dex
        for pokemon in dex_data["results"]:
            try:
                poke_response = requests.get(url=pokemon["url"])
                poke_response.raise_for_status()
                poke_data = poke_response.json()

                # Create or get Pokémon
                poke_object, created = Pokemon.objects.get_or_create(
                    id=poke_data["id"],
                    defaults={
                        "name": poke_data["name"],
                        "hp": poke_data["stats"][0]["base_stat"],
                        "attack": poke_data["stats"][1]["base_stat"],
                        "defense": poke_data["stats"][2]["base_stat"],
                        "special_attack": poke_data["stats"][3]["base_stat"],
                        "special_defense": poke_data["stats"][4]["base_stat"],
                        "speed": poke_data["stats"][5]["base_stat"],
                        "sprites": poke_data["sprites"].get("front_default", "No sprite available"),
                    }
                )

                # Add Pokémon to the bulk list
                if created:
                    bulk_pokemon.append(poke_object)
                    logger.info(f"Added pokemon: {poke_data['name']}")
                else:
                    logger.info(f"Pokemon already exists: {poke_data['name']}")

                # Create or get abilities
                abilities_to_add = []
                for ability in poke_data["abilities"]:
                    ability_object, created = Ability.objects.get_or_create(name=ability["ability"]["name"])
                    if created:
                        bulk_abilities.append(ability_object)
                        logger.info(f"Added ability: {ability['ability']['name']}")
                    else:
                        logger.info(f"Ability already exists: {ability['ability']['name']}")
                    abilities_to_add.append(ability_object)

                poke_object.abilities.add(*abilities_to_add)

                # Create or get types
                types_to_add = []
                for poke_type in poke_data["types"]:
                    type_object, created = Type.objects.get_or_create(name=poke_type["type"]["name"])
                    if created:
                        bulk_types.append(type_object)
                        logger.info(f"Added type: {poke_type['type']['name']}")
                    else:
                        logger.info(f"Type already exists: {poke_type['type']['name']}")
                    types_to_add.append(type_object)

                poke_object.types.add(*types_to_add)

                # Create or get moves
                move_urls = [move["move"]["url"] for move in poke_data["moves"]]
                for move_url in move_urls:
                    move_response = requests.get(url=move_url)
                    move_response.raise_for_status()
                    move_data = move_response.json()

                    type_obj, created = Type.objects.get_or_create(name=move_data["type"]["name"])
                    move_object, created = Move.objects.get_or_create(
                        name=move_data["name"],
                        defaults={
                            "type": type_obj,
                            "power": move_data.get("power", 0),
                            "pp": move_data.get("pp", 0),
                            "accuracy": move_data.get("accuracy", 0),
                        }
                    )
                    if created:
                        bulk_moves.append(move_object)
                        logger.info(f"Added move: {move_data['name']}")
                    else:
                        logger.info(f"Move already exists: {move_data['name']}")

                    poke_object.moves.add(move_object)

                # Log creation
                if created:
                    logger.info(f"Created new Pokémon: {poke_object.name} (ID: {poke_object.id})")
                else:
                    logger.info(f"Updated existing Pokémon: {poke_object.name} (ID: {poke_object.id})")

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching data for {pokemon['name']}: {str(e)}")
                continue

        # Perform bulk inserts to reduce database interactions
        if bulk_pokemon:
            Pokemon.objects.bulk_create(bulk_pokemon)
            logger.info(f"Bulk created {len(bulk_pokemon)} Pokémon.")
        else:
            logger.info("No Pokémon to create.")

        if bulk_abilities:
            Ability.objects.bulk_create(bulk_abilities)
            logger.info(f"Bulk created {len(bulk_abilities)} abilities.")
        else:
            logger.info("No abilities to create.")

        if bulk_types:
            Type.objects.bulk_create(bulk_types)
            logger.info(f"Bulk created {len(bulk_types)} types.")
        else:
            logger.info("No types to create.")

        if bulk_moves:
            Move.objects.bulk_create(bulk_moves)
            logger.info(f"Bulk created {len(bulk_moves)} moves.")
        else:
            logger.info("No moves to create.")

        logger.info("Database population completed.")