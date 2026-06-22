from .main import Pokemon, Stats, Move, TypeRelations, CombatEngine

def test_all_type_chart_values():
    relations = TypeRelations()
    
    for attack_type, defenders in relations.type_chart.items():
        for defender_type, expected in defenders.items():
            assert relations.get_effectiveness(attack_type, [defender_type]) == expected

def test_super_effective():
    relations = TypeRelations()
    assert relations.get_effectiveness("Fire", ["Grass"]) == 2.0

def test_normal_effective():
    relations = TypeRelations()
    assert relations.get_effectiveness("Electric", ["Fire"]) == 1.0

def test_not_very_effective():
    relations = TypeRelations()
    assert relations.get_effectiveness("Fire", ["Water"]) == 0.5

def test_immunity():
    relations = TypeRelations()
    assert relations.get_effectiveness("Electric", ["Ground"]) == 0.0

def test_dual_type_multiplies_effects():
    relations = TypeRelations()
    assert relations.get_effectiveness("Water", ["Fire", "Ground"]) == 4.0

def test_unknown_type():
    relations = TypeRelations()
    assert relations.get_effectiveness("Psychic", ["Fire"]) == 1.0


#Verificación de CombatEngine

def test_hit_accuracy():
    move = Move("Thunderbolt", "Electric", 10, 100, 10)

    hit, multiplier = CombatEngine.hit_accuracy(move, ["Ground"])
    assert multiplier == 0.0

def test_super_effective_attack():
    attacker = Pokemon("Charmander", ["Fire"], Stats(attack=10, defense=1))

    grass_target = Pokemon("Bulbasaur", ["Grass"], Stats(hp=100, defense=1))
    water_target = Pokemon("Squirtle", ["Water"], Stats(hp=100, defense=1))

    move = Move("Flame Burst", "Fire", 10, 100, 10)

    damage_grass = CombatEngine.calculate_damage(attacker, grass_target, move)
    damage_water = CombatEngine.calculate_damage(attacker, water_target, move)

    assert damage_grass > damage_water

def test_higher_power_deals():
    attacker = Pokemon("Charmander", ["Fire"], Stats(attack=10, defense=1))
    defender = Pokemon("Bulbasaur", ["Grass"], Stats(hp=100, defense=1))

    weak_move = Move("Weak", "Fire", 10, 100, 10)
    strong_move = Move("Strong", "Fire", 20, 100, 10)

    weak_damage = CombatEngine.calculate_damage(attacker, defender, weak_move)
    strong_damage = CombatEngine.calculate_damage(attacker, defender, strong_move)

    assert strong_damage > weak_damage #Aquí estamos viendo si hay una relación proporcional entre el ataque y el daño.

def test_higher_attack_stat_deals():
    weak_attacker = Pokemon("Charmander", ["Fire"], Stats(attack=5, defense=1))
    strong_attacker = Pokemon("Charmander", ["Fire"], Stats(attack=20, defense=1))
    defender = Pokemon("Bulbasaur", ["Grass"], Stats(hp=100, defense=1))

    move = Move("Flame Burst", "Fire", 10, 100, 10)

    weak_damage = CombatEngine.calculate_damage(weak_attacker, defender, move)
    strong_damage = CombatEngine.calculate_damage(strong_attacker, defender, move)

    assert strong_damage > weak_damage #Probamos que entre más ataque se genere más daño

def test_higher_defense():
    defender_higher_defense = Pokemon("Bulbasaur", ["Grass"], Stats(hp=100, defense=5))
    defender_lower_defense = Pokemon("Bulbasaur", ["Grass"], Stats(hp=100, defense=1))
    attacker = Pokemon("Charmander", ["Fire"], Stats(attack=5, defense=1))

    move = Move("Flame Burst", "Fire", 10, 100, 10)

    damage_higher_def = CombatEngine.calculate_damage(attacker, defender_higher_defense, move)
    damage_lower_def = CombatEngine.calculate_damage(attacker, defender_lower_defense, move)

    assert damage_lower_def > damage_higher_def

def test_immune_attack():
    attacker = Pokemon("Pikachu", ["Electric"], Stats(attack=10, defense=1))
    defender = Pokemon("Geodude", ["Ground"], Stats(hp=100, defense=1))

    move = Move("Thunderbolt", "Electric", 10, 100, 10)

    damage = CombatEngine.calculate_damage(attacker, defender, move)

    assert damage == 0






        



