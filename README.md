# POKE

# Resolución Actividad 1: Clase Pokemon  📚
## Objetivos 📌
1. Desarrollar la clase Pokemon.
2. Definir 10 características que posee la clase Pokemon.
3. Definir 3 Acciones que puede realizar la clase Pokemon.
4. Proponer su estructura constructor.
5. Elaborar un diagrama tipo UML inicial de la clase.
6. Los atributos tengan sentido dentro del modelo.
7. Los métodos sean realistas e implementables.

> Cómo cumplimiento de los objetivos se hace entrega del presente documento, donde se trazó todo el curso y puesta en marcha del procedimiento. 
---

## Tabla de contenidos
- [Contextualización](#contextualizacion)
- [Diseño de clase](#diseño-de-clase)
- [Diagrama UML](#diagrama-uml)


## Contextualizacion

Para dar un buen inicio, se debe comprender el cómo se usaría la teoría de Pokémon y por qué este es un buen método para el aprendizaje de la Programación Orientada a objetos.

#### ¿Porqué POO en Pokemon? 🤔

La programación orientada a objetos se basa en la modelación dinámica de desarrollo de procesos cómo evolución de la programación estructurada, 
es decir, nos da la posiblidad de realizar un proceso más eficiente, reflejando e interpretando fielmente el mundo real. 

Nos facilita la comprensión y el modelado de entidades del mundo real en la codificación de estas en el mundo virtual, esto a traves de clases cómo plantillas formadoras de objetos, abstrayendo la esencia de una entidad a partir de atributos que la caracterizan y las acciones que puede realizar.

**Pokemon** Es una franquicia iniciada cómo un videojuego RPG, donde en un mundo alternativo los humanos conviven con criaturas ficticias, capturándolas, entrenándolas y utilizándolas para combatir entre sí.

A partir de esto, logramos ver que pokemon funciona con reglas lógicas y relaciones que encajan muy bien en los pilares fundamentales de la **POO**:

- Abstracción: Al ser pokemon un mundo alternativo imaginario, logramos abstraer la esencia de este, que son los pokemones, y logramos identificarlos bajo sus atributos relevantes y las acciones que logran hacer.
  
- Herencia: Podemos observar que todos los pokemones comparten rasgos, pero a sus vez tienen especializaciones que los diferencian a cada uno, por lo tanto somos capaces de a partir una *Clase* general, generar otra que **herede** de está sus características y que forme otras nuevas que la especializen.

- Polimorfismo: A su vez aquellas herencias de la clase padre pueden cambiar, pues todos los pokemones son capaces de *atacar()* más todos atacan distinto.

- Encapsulamiento: Finalmente, varias de las características que poseen los pokemones no se pueden cambiar si no a partir de procesos, y no todos pueden cambiarla, por lo tanto estas deben tener características protegidas, privadas o públicas para modificarlas dependientemente.

En sintesís, Pokemon es capaz de abstraer criaturas ficticias y relacionarlas entre sí basandose en sus clases especificas heredadas de su identidad común, evolucionar y comportarse de módo diferente con respecto a una condición, lo cual aporta significativamente a una comprensión de lo que es La poo
puesto que está se basa en simbolizar objetos generales y llevar a cabo procesos especializados entre sus individualidades.

## Diseño de clase 

A partir de lo descrito, Basándonos en la franquicia y videojuegos de pokemon, se propone cómo clase principal para nuestro diseño la entidad *POKEMON*, abstraida con atributos generales cómo: 

- *Puntos de vida* : Al ser una entidad viva capacitada para combatir, nos basamos en los puntos de vida cómo parametro de control, el cuál cambiara su valor constantemente durante un combate.
- *Tipo* : Atributo general que define los diversos caminos de cómo interactuará un pokemon en el entorno.
- *Nombre*: Puesto que todo objeto necesita un identificador legible para el usuario y diferenciable de todo pokemon.
- *Aspecto* : Característica que permite visualizar con mayor detalle a cada objeto.
- *Fuerza base:*: Capacidad de influencia a otro objeto pokemon, que toda instanciación debera tener.
- *Nivel* : Atributo pivote, capaz de moderar los atributos generales del pokemon, modificable a partir de una acción de mejora que posea el pokemon.
- *Capacidad de defensa* : Al igual que el pokemon es capaz de influir a otro, este tambien es condicionado contra otro objeto, por lo que el atributo *capacidad de defensa* logra controlar más la interacción de combate entre pokemones.
- *Habilidad especial* : Como medio de ataque el pokémon poseerá una habilidad individual que altere la fuerza y resistencia del pokemon, generando mayor diversidad y campo de juego en las relaciones.
- *Ataques*  : Acciones consecutivas en el campo de batalla, cada una poseerá una característica especial, aumentando la variabilidad de sus estadísticas.
- *Evolución* : Medida importante que rastrea el desarrollo del objeto, capaz de modificar su atributo *Nivel* a partir de una acción controlada.

Finalmente, aunque muchas características sean bienvenidas, se consideran cómo las fundamentales y generales para la relación de un pokemon en el mundo virtual.

Por otro lado, a partir de estás características, el pokemon se comportará en un ambiente de combate con acciones que todos los objetos poseen:  
- ***Attack(target: Pokemon, attack_power: float): void***  
Acción fundamental para la interacción entre objetos. Permite que un pokemon ataque a otro, reduciendo sus puntos de vida.  
***Parametros***:  
-target (Pokemon): Pokemon que recibirá el ataque.  
-attack_power (float): Cantidad de daño que se aplicará al objetivo.  
  
- ***Defend(damage_received: float): void***  
Acción que permite al pokemon reducir el daño recibido durante un ataque, utilizando su capacidad de defensa.  
***Parámetros***:  
damage_received (float):  Cantidad de daño que el pokemon recibe antes de aplicar la defensa.  

- ***Evolve(new_level: int, new_ability: str): void***  
Acción que permite al pokemon aumentar su nivel y mejorar sus estadísticas, pudiendo también adquirir una nueva habilidad especial.  
***Parámetros***:  
-new_level (int): Nivel al que evolucionará el pokemon.  
-new_ability (str): Nueva habilidad que puede adquirir al evolucionar.  

---

### Sintesis
Proponemos la siguiente clase *Pokemon* que afianza la interpretación de un Pokemon con las características que todos estos tienen, capaces de interactuar y afectarse entre ellos, por lo que se propone la estructura de la construcción de la plantilla de la siguiente manera.

#### constructor de clase pokemon
 Parametros  de entrada:
 - health_points (int): default = 10 
 - base_strength (float): default = 1
 - defense_capacity (float): default = 0.5
 - level (int): default = 1
 - type (str): variable, asignable por el entorno
 - appearance (str): variable, asignable por el retorno
 - special_ability (str): variable, default = ninguno

de forma que una sintaxis correcta seria: 

```bash
- CONSTRUCTOR(health_points: int, base_strength: float, defense_capacity: float,
            level: int, type: str, appearance: str, special_ability: str)
```

--- 

## Diagrama UML
```mermaid
classDiagram
    direction TB

    class Pokemon {
        -name: str
        -type: str
        -health_points: int
        -base_strength: float
        -level: int
        -defense_capacity: float
        -appearance: str
        -special_ability: str
        -attacks: list
        -evolution_stage: int

        +Pokemon(health_points: int, base_strength: float, defense_capacity: float, level: int, type: str, appearance: str, special_ability: str) 

        +attack(target: Pokemon, attack_power: float): void
        +defend(damage_received: float): void
        +evolve(new_level: int, new_ability: str): void
    }
```
Se utiliza los tres metodos principales de ataque, defensa y evolucionar, con sus respectivos atributos para controlar el comportamiento del pokemon en el entorno de combate, además de los atributos generales que caracterizan a cada pokemon.

Siendo valido que se puedan usar estos metodos, aunque en el futuro se puedan agregar más, pero estos son los generales para la interacción entre pokemones.
