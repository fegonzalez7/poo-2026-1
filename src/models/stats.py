class Stats:
    def __init__(
        self,
        hp: float,
        attack: float,
        defense: float,
        special_attack: float,
        special_defense: float,
        speed: float,
    ):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

    def __str__(self):
        return (
            f"HP: {self.hp}, "
            f"Attack: {self.attack}, Defense: {self.defense}, "
            f"Sp. Attack: {self.special_attack}, Sp. Defense: {self.special_defense}, "
            f"Speed: {self.speed}"
        )
