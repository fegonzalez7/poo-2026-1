import random
from typing import List

from src.engine.type_relations import TypeRelations
from src.models.move import Move
from src.models.pokemon import Pokemon


class CombatEngine:
    """
    Implementa los metodos para el calculo de damage y una funcion
    con numeros pseudoaleatorios para definir cuando se falla un ataque

    Asumiendo que existe class Move con las siguientes caracteristicas:
    Move: Debe contener los atributos de un ataque: name, type (string), power,
    accuracy, y pp.
    """

    @staticmethod
    def hit_accuracy(attack: Move, defender_types: List[str]) -> tuple[bool, float]:
        tp = TypeRelations()
        effect = tp.get_effectiveness(attack.type, defender_types)
        factor = random.random()

        hit_chance = max(0.0, min(1.0, attack.accuracy / 100))
        return factor < hit_chance, effect  # True si el ataque acierta

    @staticmethod
    def calculate_damage(attacker: Pokemon, defender: Pokemon, move: Move):
        att_stats = attacker.stats
        def_stats = defender.stats
        is_able_to_attack, multiplier = CombatEngine.hit_accuracy(move, defender.types)
        # tener en cuenta quien tiene mas nivel
        rlevel = attacker.level / defender.level
        # tener en cuenta si atacante tiene mas ataque que la defensa del defensa
        rdef = att_stats.attack / max(def_stats.defense, 1e-9)
        # ataque -> si is_able_to_attack = 0 entonces ataque fallido, sino, calcular ataque
        damage = int(is_able_to_attack) * (rlevel * rdef * multiplier * move.power)
        print(f"Damage: {damage}")
        return damage
