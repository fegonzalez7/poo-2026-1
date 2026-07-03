# POKE — Sistema de Combate Pokémon

Sistema didáctico de combate tipo Pokémon construido en Python 3.10+,
diseñado para ilustrar los principios fundamentales de la Programación
Orientada a Objetos (POO).

---

## Tabla de contenidos

- [Objetivos](#objetivos)
- [Principios POO aplicados](#principios-poo-aplicados)
- [Estructura de módulos y paquetes](#estructura-de-módulos-y-paquetes)
- [Diseño del sistema](#diseño-del-sistema)
- [Diagrama UML](#diagrama-uml)
- [Instrucciones de uso](#instrucciones-de-uso)
- [Contribuir](#contribuir)

---

## Objetivos

1. Modelar un sistema de combate tipo Pokémon usando los principios de POO.
2. Definir clases con responsabilidades claras y bien delimitadas.
3. Representar relaciones entre entidades (composición, agregación, herencia) mediante UML.
4. Organizar el código en módulos y paquetes reutilizables.

---

## Principios POO aplicados

### 1. Encapsulamiento

Cada clase protege su estado interno y expone solo lo necesario:

- `Move` declara todos sus atributos como privados (`_name`, `_type`, `_power`,
  `_accuracy`, `_pp`) y los expone a través de `@property`, impidiendo
  modificaciones externas accidentales.
- `Moveset` controla toda la lista interna de movimientos; la única forma de
  agregar o reemplazar un movimiento es a través de sus métodos públicos
  (`add_move`, `replace_move`, `remove_move`), que aplican la restricción de
  máximo cuatro movimientos.
 - `Pokemon` mantiene su estado de combate (vida, nivel, habilidad especial) y delega las estadísticas a un objeto `Stats`.

### 2. Abstracción

Cada clase modela únicamente los conceptos necesarios para su responsabilidad:

- `Stats` encapsula el conjunto completo de estadísticas de combate en un
  único objeto, simplificando la firma del constructor de `Pokemon`.
- `CombatEngine` abstrae toda la lógica de cálculo de daño y precisión en nuevos
  métodos.
- `TypeRelations` abstrae la tabla de efectividades de tipos en una consulta
  simple (`get_effectiveness`), ocultando la estructura interna del diccionario.

### 3. Herencia

La clase `Pokemon` actúa como clase base:

- `Charmander` hereda de `Pokemon` y sobrescribe nombre, tipos y estadísticas
  predeterminadas al evolucionar, reutilizando toda la lógica de combate y evolución del padre.

### 4. Polimorfismo

`CombatEngine.calculate_damage()` recibe objetos `Pokemon` sin depender de implementaciones concretas; cualquier subclase futura de `Pokemon` podrá usarse sin cambiar la lógica del motor.

### 5. Composición y Agregación

- **Composición fuerte** (`*--`): `Pokemon` posee un `Stats` y un `Moveset`
  que no tienen sentido fuera del Pokémon que los contiene. Si el Pokémon es
  eliminado, sus estadísticas y moveset dejan de existir.
- **Composición fuerte** (`*--`): `Moveset` posee sus `Move`; un movimiento
  pertenece a un único Moveset.
- **Agregación** (`o--`): `Trainer` gestiona una lista de Pokémon, pero los
  Pokémon pueden existir independientemente. `Field` referencia a los dos `Trainer` sin apropiarse de ellos;
los Pokémon activos se obtienen dinámicamente durante la batalla.

---

## Estructura de módulos y paquetes

```
poke-repo/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pokemon.py       
│   │   ├── pokemon_types.py 
│   │   ├── move.py          
│   │   ├── stats.py         
│   │   └── trainer.py       
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── combat_engine.py  
│   │   ├── type_relations.py 
│   │   └── field.py          
│   └── utils/
│       ├── __init__.py
│       └── constants.py      
├── tests/
│   ├── __init__.py
│   ├── test_combat_engine.py
│   ├── test_battle_flow.py
│   └── test_evolution.py
├── README.md                   
├── requirements.txt
└── main.py
```

### Responsabilidad de cada módulo

| Módulo | Responsabilidad |
|---|---|
| `models/pokemon.py` | Entidad principal: atributos, combate, evolución y ganancia de experiencia |
| `models/move.py` | Representación de movimientos y colección de hasta 4 moves |
| `models/stats.py` | Contenedor de estadísticas de combate |
| `models/trainer.py` | Gestión de equipo (hasta 6 Pokémon) y cambio de activo |
| `engine/combat_engine.py` | Cálculo de daño, comprobación de precisión |
| `engine/type_relations.py` | Tabla de efectividades entre tipos |
| `utils/constants.py` | Valores globales reutilizables |

---

## Diseño del sistema

### Entidades principales

| Clase | Rol |
|---|---|
| `Pokemon` | Entidad combatiente con estadísticas, moveset y lógica de evolución |
| `Stats` | Encapsula HP, ataque, defensa, velocidad y ataque especial |
| `Move` | Representa un movimiento con nombre, tipo, poder, precisión y PP |
| `Moveset` | Colección de hasta 4 movimientos con operaciones de gestión |
| `Trainer` | Gestor de equipo de hasta 6 Pokémon |
| `CombatEngine` | Lógica de cálculo de daño y verificación de impacto |
| `TypeRelations` | Tabla de multiplicadores de tipo (fuego, agua, planta…) |

---

## Diagrama UML del proyecto:


```mermaid
classDiagram
  direction TB

  class Stats {
    +hp : float
    +attack : float
    +defense : float
    +special_attack : float
    +special_defense : float
    +speed : float
    +__str__() str
  }

  class Move {
    -_name : str
    -_type : str
    -_power : float
    -_accuracy : int
    -_pp : int
    +name() str
    +type() str
    +power() float
    +accuracy() int
    +pp() int
  }

  class Moveset {
    -moves : List~Move~
    +add_move(move) bool
    +remove_move(index) bool
    +replace_move(index, new_move) bool
    +get_moves() List~Move~
    +show_moves() None
  }

  class Pokemon {
    +name : str
    +types : List~str~
    +life : float
    +attack_power : float
    +defense : float
    +level : int
    +special_ability : str
    +stats : Stats
    +moveset : Moveset
    +get_stats() str
    +attack(target, move, relations) None
    +defender(damage) None
    +evolve(new_level, new_ability) None
  }

  class Trainer {
    +nombre : str
    +team : str
    +pokemon : List~Pokemon~
    +add_pokemon(pokemon) None
    +get_active_pokemon() Pokemon
    +switch_pokemon(pokemon_index) None
  }

  class TypeRelations {
    -type_chart : dict
    +get_effectiveness(attack_type, defender_types) float
  }

  class CombatEngine {
    <<static>>
    +hit_accuracy(attack, defender_types)$ tuple~bool, float~
    +calculate_damage(attacker, defender, move)$ float
  }

  Pokemon *-- Stats : contains
  Pokemon *-- Moveset : contains
  Moveset *-- Move : 0..4
  Trainer o-- Pokemon : 1..6
  CombatEngine ..> Move : uses
  CombatEngine ..> Pokemon : uses
  CombatEngine ..> TypeRelations : delegates
  Pokemon ..> TypeRelations : uses
```

### Notación utilizada

| Símbolo | Significado |
|---|---|
| `*--` | Composición — la parte no existe sin el todo |
| `o--` | Agregación — la parte puede existir de forma independiente |
| `-->` | Dependencia — una clase usa otra sin poseerla |
| `<\|--` | Herencia — la subclase extiende la superclase |
| `<<static>>` | La clase no se instancia; sus métodos son estáticos |
| `-` prefijo | Atributo o método privado |
| `+` prefijo | Atributo o método público |

---

## Instrucciones de uso

### Requisitos previos

- Python 3.10 o superior
- Administrador de paquetes de Python **`uv`** instalado en el sistema

### Instalación y Configuración

1. Primero debemos clonar el repositorio y navega a la carpeta del proyecto:
```bash
git clone https://github.com/fegonzalez7/poo-2026-1.git
cd poo-2026-1
```

2. Como segundo paso, se crea el entorno virtual aislado utilizando `uv`:
```bash
uv venv
```

3. Luego, se instala las dependencias lógicas del proyecto y las herramientas de desarrollo (`pytest`, `ruff`, `mypy`):
```bash
uv pip install -r requirements.txt
uv pip install pytest mypy ruff
```

### Ejecutar la simulación

Para iniciar el simulador de combate Pokémon, ejecuta el script principal a través del entorno virtual:
```bash
uv run python main.py
```

Durante la ejecución, el juego pedirá por consola qué movimiento usar en cada turno y si deseas continuar, cambiar de Pokémon o rendirte.

### Ejecutar los tests

Para validar que los componentes y la lógica funcionen correctamente:
```bash
uv run python -m pytest
```

### Aseguramiento de Calidad 

El proyecto utiliza un pipeline estricto para validar el formato y el tipado, este se puede comprobar localmente con:

- **Verificación de Estilo y Formato (Ruff):**
  ```bash
  uv run ruff format --check .
  uv run ruff check .
  ```

- **Verificación de Tipado Estático (Mypy):**
  ```bash
  uv run mypy .
  ```