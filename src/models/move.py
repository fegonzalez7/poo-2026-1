import time
from typing import List


class Move:
    def __init__(self, name: str, type: str, power: float, accuracy: int, pp: int):
        self._name = name
        self._type = type
        self._power = power
        self._accuracy = accuracy
        self._pp = pp

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def power(self) -> float:
        return self._power

    @property
    def accuracy(self) -> int:
        return self._accuracy

    @property
    def pp(self) -> int:
        return self._pp


class Moveset:
    def __init__(self, moves: List[Move] | None = None):
        self.moves: List[Move] = []
        if moves:
            for move in moves:
                self.add_move(move)

    def add_move(self, move: Move) -> bool:
        if len(self.moves) < 4:
            self.moves.append(move)
            print(f"¡El Pokémon aprendió {move.name}!")
            time.sleep(0.5)
            return True
        else:
            print(f"El Pokémon intenta aprender {move.name}, pero tiene 4 movimientos.")
            time.sleep(0.5)
            return False

    def remove_move(self, index: int) -> bool:
        if 0 <= index < len(self.moves):
            removed_move = self.moves.pop(index)
            print("1, 2 y... ¡Poof!")
            time.sleep(1)
            print(f"El Pokémon olvidó cómo usar {removed_move.name}.")
            time.sleep(0.5)
            return True
        else:
            print("Índice no válido. No se pudo olvidar el movimiento.")
            return False

    def replace_move(self, index: int, new_move: Move) -> bool:
        if 0 <= index < len(self.moves):
            old_move = self.moves[index]
            print("1, 2 y... ¡Poof!")
            time.sleep(1)
            print(f"El Pokémon olvidó cómo usar {old_move.name} y...")
            time.sleep(1)
            self.moves[index] = new_move
            print(f"¡Aprendió {new_move.name}!")
            time.sleep(0.5)
            return True
        else:
            print("Índice no válido. No se pudo reemplazar el movimiento.")
            return False

    def get_moves(self) -> List[Move]:
        return self.moves

    def show_moves(self) -> None:
        if not self.moves:
            print("El Pokémon aún no conoce ningún movimiento.")
            time.sleep(0.5)
        else:
            print("\n" + "=" * 45)
            print("                 MOVIMIENTOS")
            print("=" * 45)
            for i, move in enumerate(self.moves):
                print(
                    f"[{i + 1}] {move.name.ljust(12)} | Tipo: {move.type.ljust(8)}"
                    f"| Poder: {str(move.power).ljust(3)} | PP: {move.pp}"
                )
            print("=" * 45 + "\n")
            time.sleep(0.5)
