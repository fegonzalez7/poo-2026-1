from main import Pokemon, Stats, Moveset, Move


def make_charmander(level=1):
    stats = Stats(hp=20, attack=2, defense=0.3, special_attack=1, special_defense=1, speed=2)
    move = Move(name="Flame Burst", type="Fire", power=5, accuracy=100, pp=25)

    return Pokemon("Charmander", ["Fire"], stats, life=stats.hp, level=level,
                    moveset=Moveset([move]))


def test_evolve_increases_level_to_correct_value():
    charmander = make_charmander(level=1)

    charmander.evolve(5, "Blaze")

    assert charmander.level == 5


def test_evolve_sets_new_special_ability():
    charmander = make_charmander(level=1)

    charmander.evolve(5, "Blaze")

    assert charmander.special_ability == "Blaze"


def test_evolve_does_not_change_level_when_target_level_is_equal():
    charmander = make_charmander(level=5)

    charmander.evolve(5, "Blaze")

    assert charmander.level == 5
    assert charmander.special_ability == "None"  # No cambia porque no evolucionó


def test_evolve_does_not_change_level_when_target_level_is_lower():
    charmander = make_charmander(level=5)

    charmander.evolve(3, "Blaze")

    assert charmander.level == 5
    assert charmander.special_ability == "None"


def test_evolve_does_not_change_name_or_type():
    charmander = make_charmander(level=1)

    charmander.evolve(5, "Blaze")

    assert charmander.name == "Charmander"
    assert charmander.types == ["Fire"]


def test_evolve_keeps_moveset_intact():
    charmander = make_charmander(level=1)
    original_moves = charmander.moveset.get_moves()

    charmander.evolve(5, "Blaze")

    assert charmander.moveset.get_moves() == original_moves


def test_evolve_does_not_change_current_life():
    charmander = make_charmander(level=1)
    life_before = charmander.life

    charmander.evolve(5, "Blaze")

    assert charmander.life == life_before


def test_multiple_sequential_evolutions_reach_final_level():
    charmander = make_charmander(level=1)

    charmander.evolve(3, "Blaze")
    charmander.evolve(5, "Solar Power")

    assert charmander.level == 5
    assert charmander.special_ability == "Solar Power"


def test_evolve_returns_none():
    charmander = make_charmander(level=1)

    result = charmander.evolve(5, "Blaze")

    assert result is None
