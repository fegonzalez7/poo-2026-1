from .main import Pokemon, Stats, Moveset, Move, Charmeleon

def make_charmander ():
    stats = Stats(hp=20, attack=2, defense=0.3, special_attack=1, special_defense=1, speed=2)
    stats_max = Stats(hp=28, attack=3.5, defense=0.5, special_attack=2, special_defense=2, speed=3.5)
    move = Move(name="Flame Burst", type="Fire", power=5, accuracy=100, pp=25)

    return Pokemon("Charmander", ["Fire"], stats, stats_max, moveset=Moveset([move]), evolution="Charmeleon", evolution_level=5,)

def exp_needed_for_level(target_level: int):
    total = 0
    for level in range (1, target_level):
        total +=level * 10

    return total

def test_pokemon_levels():
    charmander = make_charmander()

    exp_for_one_level = exp_needed_for_level(2)
    result = charmander.gain_experience(exp_for_one_level)

    assert charmander.level == 2
    assert result is None #Porque subir de nivel no necesariamente hace que el pokemon evolucione

def test_pokemon_evolves_at_correct_level():
    charmander = make_charmander()

    exp_for_evolution_level = exp_needed_for_level(5)  
    result = charmander.gain_experience(exp_for_evolution_level)

    assert result is not None
    assert isinstance(result, Charmeleon)
    assert result.name == "Charmeleon"
    assert result.level == 5 #Nos surge una duda, ¿al evolucionar se mantiene el nivel? Porque no lo está haciendo, y por ende este test falla

def test_pokemon_does_not_evolve_before_evolution_level():
    charmander = make_charmander()

    exp_before_evolution = exp_needed_for_level(4)  
    result = charmander.gain_experience(exp_before_evolution)

    assert charmander.level == 4
    assert result is None
    assert isinstance(charmander, Pokemon)
    assert not isinstance(charmander, Charmeleon)

def test_evolved_pokemon_keeps_moveset_and_experience():
    charmander = make_charmander()

    original_moves = charmander.moveset.get_moves()

    evolved = charmander.gain_experience(exp_needed_for_level(5))

    assert evolved.moveset.get_moves() == original_moves
    assert evolved.experience == charmander.experience

def test_pokemon_does_not_level_up_with_insufficient_xp():
    charmander = make_charmander()

    charmander.gain_experience(5)

    assert charmander.level == 1

def test_pokemon_does_not_evolve_before_required():
    charmander = make_charmander()

    exp_before = exp_needed_for_level(5) - 1
    result = charmander.gain_experience(exp_before)

    assert result is None
    assert charmander.level < 5

def test_evolved_pokemon_keeps_type():
    charmander = make_charmander()

    evolved = charmander.gain_experience(exp_needed_for_level(5))

    assert evolved.types == ["Fire"]

def test_remaining_experience_is_preserved_after_level_up():
    charmander = make_charmander()

    charmander.gain_experience(15)

    assert charmander.level == 2
    assert charmander.experience == 5

def test_multiple_level_ups():
    charmander = make_charmander()

    charmander.gain_experience(30) #Puesto que para pasar a nivel 2 necesita 10 y para pasar de nivel 2 a 3 necesita 20

    assert charmander.level == 3

def test_stats_increase_after_level_up():
    charmander = make_charmander()

    attack_before = charmander.stats.attack
    charmander.gain_experience(10)

    assert charmander.stats.attack > attack_before



