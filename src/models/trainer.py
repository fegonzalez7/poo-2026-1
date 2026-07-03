from typing import List

from src.models.pokemon import Pokemon


class Trainer:
    def __init__(self, nombre: str, team: str, pokemon: List[Pokemon]):
        self.nombre = nombre
        self.team = team
        self.pokemon = pokemon if pokemon is not None else []

    def add_pokemon(self, pokemon: Pokemon):
        if len(self.pokemon) < 6 and pokemon not in self.pokemon:
            self.pokemon.append(pokemon)
        else:
            print("No se puede agregar más Pokémon o el Pokémon ya está en el equipo.")

    def get_active_pokemon(self):
        if self.pokemon:
            return self.pokemon[0]
        else:
            print("No tienes Pokémon en tu equipo.")
            return None

    def switch_pokemon(self, pokemon_index):
        if 0 <= pokemon_index < len(self.pokemon):
            self.pokemon[0], self.pokemon[pokemon_index] = (
                self.pokemon[pokemon_index],
                self.pokemon[0],
            )
        else:
            print("Indice de Pokémon no valido.")
