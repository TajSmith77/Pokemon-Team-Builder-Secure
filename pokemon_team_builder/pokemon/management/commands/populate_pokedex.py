### A management command for populating the pokedex table with pokemon data from the PokeAPI #####

import requests
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon, Type, Move, Ability

class Command(BaseCommand):
    help = 'Fetches Pokemon data from PokeAPI and inserts it into the pokedex table'
    def handle(self, *args, **options):

        
        
        # Fetch Pokemon dex data from PokeAPI
        dex_response = requests.get(url="https://pokeapi.co/api/v2/pokemon/?&limit=1025")
        dex_response.raise_for_status()
        dex_data = dex_response.json()

        # Insert the pokemon data into the table
        for pokemon in dex_data["results"]:
            poke_response = requests.get(url=pokemon["url"])
            poke_response.raise_for_status()
            poke_data = poke_response.json()


            #Create or get pokemon
            poke_object, created = Pokemon.objects.get_or_create(
                id = poke_data["id"],
                defaults={
                    "name": poke_data["name"],
                    "hp": poke_data["stats"][0]["base_stat"],
                    "attack": poke_data["stats"][1]["base_stat"],
                    "defense": poke_data["stats"][2]["base_stat"] ,
                    "special_attack": poke_data["stats"][3]["base_stat"],
                    "special_defense": poke_data["stats"][4]["base_stat"] ,
                    "speed": poke_data["stats"][5]["base_stat"],
                    "sprites": poke_data["sprites"].get("front_default", "No sprite available"),
                }
            )
            #Create or get abilities
            for ability in poke_data["abilities"]:
                ability_object, created = Ability.objects.get_or_create(
                    name = ability["ability"]["name"]
                )
                poke_object.abilities.add(ability_object)

            #Create or get types
            for type in poke_data["types"]:
                type_object, created = Type.objects.get_or_create(
                    name = type["type"]["name"]
                )
                poke_object.types.add(type_object)


            #Create or get moves
            move_urls = [move["move"]["url"] for move in poke_data["moves"]]
            for move_url in move_urls:
                move_response = requests.get(url=move_url)
                move_response.raise_for_status()
                move_data = move_response.json()

                
                type_obj, created = Type.objects.get_or_create(name=move_data["type"]["name"])
                move_object, created = Move.objects.get_or_create(
                    name = move_data["name"] if "name" in move_data else None,
                    defaults={
                        "type": type_obj,
                        "power": move_data.get("power",0),
                        "pp": move_data.get("pp",0),
                        "accuracy": move_data.get("accuracy",0),
                    }

                )
                poke_object.moves.add(move_object)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created new {poke_object.name} ({poke_object.id}) hp: {poke_object.hp}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Retrieved {poke_object.name} ({poke_object.id}) hp: {poke_object.hp}"))