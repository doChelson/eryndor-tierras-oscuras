from dataclasses import dataclass, field
from typing import List


CLASES = {
    "Guerrero": {
        "descripcion": "Maestro del combate cuerpo a cuerpo. Fuerte, resistente y letal.",
        "fuerza": 16, "destreza": 12, "inteligencia": 8,
        "constitucion": 15, "sabiduria": 9, "carisma": 10,
        "hp_base": 55, "mp_base": 10,
        "dado_danio": 8, "armadura_base": 14,
        "habilidad_especial": "Golpe Poderoso",
        "desc_habilidad": "Doblas el dado de daño en tu próximo ataque",
        "costo_mp": 0,
        "color": "red",
        "icono": "[red]⚔[/red]",
    },
    "Mago": {
        "descripcion": "Canalizador de energías arcanas. Poderoso pero frágil.",
        "fuerza": 7, "destreza": 11, "inteligencia": 17,
        "constitucion": 8, "sabiduria": 13, "carisma": 11,
        "hp_base": 28, "mp_base": 55,
        "dado_danio": 10, "armadura_base": 10,
        "habilidad_especial": "Bola de Fuego",
        "desc_habilidad": "Lanzas una bola de fuego arcana (2d10 daño, cuesta 15 MP)",
        "costo_mp": 15,
        "color": "blue",
        "icono": "[blue]✦[/blue]",
    },
    "Pícaro": {
        "descripcion": "Experto en sigilo y engaño. Rápido como el viento.",
        "fuerza": 10, "destreza": 17, "inteligencia": 13,
        "constitucion": 10, "sabiduria": 10, "carisma": 13,
        "hp_base": 38, "mp_base": 20,
        "dado_danio": 6, "armadura_base": 13,
        "habilidad_especial": "Ataque Furtivo",
        "desc_habilidad": "Golpeas desde las sombras: triplicas el daño",
        "costo_mp": 0,
        "color": "green",
        "icono": "[green]✦[/green]",
    },
    "Clérigo": {
        "descripcion": "Servidor divino y sanador. La luz en la oscuridad.",
        "fuerza": 11, "destreza": 9, "inteligencia": 11,
        "constitucion": 13, "sabiduria": 16, "carisma": 14,
        "hp_base": 42, "mp_base": 40,
        "dado_danio": 6, "armadura_base": 12,
        "habilidad_especial": "Sanación Divina",
        "desc_habilidad": "Te curas 2d8 + sabiduría HP (cuesta 10 MP)",
        "costo_mp": 10,
        "color": "yellow",
        "icono": "[yellow]✦[/yellow]",
    },
    "Paladín": {
        "descripcion": "Guerrero sagrado. La fuerza del bien encarnada.",
        "fuerza": 14, "destreza": 10, "inteligencia": 9,
        "constitucion": 14, "sabiduria": 11, "carisma": 15,
        "hp_base": 48, "mp_base": 28,
        "dado_danio": 8, "armadura_base": 15,
        "habilidad_especial": "Smite Sagrado",
        "desc_habilidad": "Canalizas energía divina: +2d8 daño sagrado (cuesta 12 MP)",
        "costo_mp": 12,
        "color": "bright_white",
        "icono": "[bright_white]✦[/bright_white]",
    },
}

PREGUNTAS_PERSONALIDAD = [
    {
        "pregunta": "Ante un gran peligro, ¿cómo reaccionas?",
        "opciones": [
            ("Me lanzo al frente. Mi fuerza es mi mejor herramienta.", "fuerza", 1, "valiente"),
            ("Analizo la situación antes de actuar.", "inteligencia", 1, "sabio"),
            ("Busco una salida alternativa o una distracción.", "destreza", 1, "astuto"),
        ],
    },
    {
        "pregunta": "Un aldeano pobre te pide ayuda. ¿Qué haces?",
        "opciones": [
            ("Le doy todo lo que puedo, aunque sea poco.", "carisma", 1, "compasivo"),
            ("Lo defiendo de sus opresores sin pensarlo dos veces.", "fuerza", 1, "leal"),
            ("Evalúo sus necesidades y ofrezco lo más útil.", "sabiduria", 1, "pragmático"),
        ],
    },
    {
        "pregunta": "Encuentras un grimorio antiguo en las ruinas. ¿Qué haces?",
        "opciones": [
            ("Lo estudio con cuidado: el conocimiento es poder.", "inteligencia", 1, "curioso"),
            ("Lo destruyo. Nada bueno viene de la magia oscura.", "sabiduria", 1, "prudente"),
            ("Lo guardo para venderlo al mejor postor.", "destreza", 1, "oportunista"),
        ],
    },
    {
        "pregunta": "En pleno combate, tu aliado cae herido. ¿Qué haces?",
        "opciones": [
            ("Me interpongo entre él y el enemigo.", "constitucion", 1, "protector"),
            ("Termino la batalla rápido para poder ayudarlo.", "fuerza", 1, "determinado"),
            ("Lo cargo y lo pongo a salvo antes de seguir.", "destreza", 1, "cauteloso"),
        ],
    },
    {
        "pregunta": "¿Cuál es tu mayor motivación en la vida?",
        "opciones": [
            ("Proteger a los inocentes y hacer justicia.", "constitucion", 1, "noble"),
            ("Descubrir los secretos ocultos del mundo.", "inteligencia", 1, "explorador"),
            ("Ganar fama, poder y que todos recuerden tu nombre.", "carisma", 1, "ambicioso"),
        ],
    },
]

CLASE_RECOMENDADA = {
    "fuerza": "Guerrero",
    "inteligencia": "Mago",
    "destreza": "Pícaro",
    "sabiduria": "Clérigo",
    "constitucion": "Paladín",
    "carisma": "Paladín",
}


@dataclass
class Item:
    nombre: str
    tipo: str
    descripcion: str
    valor_oro: int = 0
    efecto: dict = field(default_factory=dict)


@dataclass
class Personaje:
    nombre: str
    clase: str

    fuerza: int = 10
    destreza: int = 10
    inteligencia: int = 10
    constitucion: int = 10
    sabiduria: int = 10
    carisma: int = 10

    nivel: int = 1
    experiencia: int = 0
    hp_max: int = 30
    hp_actual: int = 30
    mp_max: int = 20
    mp_actual: int = 20

    dado_danio: int = 6
    armadura: int = 10
    oro: int = 15

    inventario: List[Item] = field(default_factory=list)
    rasgos: List[str] = field(default_factory=list)

    habilidad_especial: str = ""
    habilidad_usos: int = 3
    habilidad_costo_mp: int = 0

    enemigos_derrotados: int = 0
    decisiones_heroicas: int = 0

    # Equipamiento
    arma_equipada: str = ""  # nombre del arma equipada
    puntos_pendientes: int = 0

    # Flags de historia
    flags: dict = field(default_factory=dict)

    @property
    def xp_siguiente_nivel(self) -> int:
        return self.nivel * 150

    @property
    def mod_fuerza(self) -> int:
        return (self.fuerza - 10) // 2

    @property
    def mod_destreza(self) -> int:
        return (self.destreza - 10) // 2

    @property
    def mod_inteligencia(self) -> int:
        return (self.inteligencia - 10) // 2

    @property
    def mod_constitucion(self) -> int:
        return (self.constitucion - 10) // 2

    @property
    def mod_sabiduria(self) -> int:
        return (self.sabiduria - 10) // 2

    @property
    def mod_carisma(self) -> int:
        return (self.carisma - 10) // 2

    @property
    def mod_ataque(self) -> int:
        return max(self.mod_fuerza, self.mod_destreza)

    @property
    def danio_min(self) -> int:
        return max(1, 1 + self.mod_ataque)

    @property
    def danio_max(self) -> int:
        return max(1, self.dado_danio + self.mod_ataque)

    @property
    def arma_actual(self):
        for item in self.inventario:
            if item.tipo == "arma" and item.nombre == self.arma_equipada:
                return item
        # Si no hay arma equipada, buscar la primera
        for item in self.inventario:
            if item.tipo == "arma":
                self.arma_equipada = item.nombre
                return item
        return None

    def armas_disponibles(self) -> list:
        return [item for item in self.inventario if item.tipo == "arma"]

    def equipar_arma(self, nombre: str) -> bool:
        for item in self.inventario:
            if item.tipo == "arma" and item.nombre == nombre:
                self.arma_equipada = item.nombre
                # Actualizar dado de daño según arma
                dado = item.efecto.get("dado_danio", self.dado_danio)
                if dado:
                    self.dado_danio = dado
                return True
        return False

    def agregar_xp(self, cantidad: int) -> bool:
        self.experiencia += cantidad
        if self.experiencia >= self.xp_siguiente_nivel:
            self._subir_nivel()
            return True
        return False

    def _subir_nivel(self):
        self.nivel += 1
        self.experiencia = 0
        aumento_hp = 8 + self.mod_constitucion
        self.hp_max += max(2, aumento_hp)
        self.hp_actual = self.hp_max
        self.mp_max += 5
        self.mp_actual = self.mp_max
        self.habilidad_usos = 3
        # Los puntos se asignan manualmente via UI
        self.puntos_pendientes = 4

    def esta_vivo(self) -> bool:
        return self.hp_actual > 0

    def curar(self, cantidad: int):
        self.hp_actual = min(self.hp_max, self.hp_actual + cantidad)

    def recibir_danio(self, cantidad: int):
        self.hp_actual = max(0, self.hp_actual - cantidad)

    def usar_mp(self, cantidad: int) -> bool:
        if self.mp_actual >= cantidad:
            self.mp_actual -= cantidad
            return True
        return False

    def tiene_pocion(self) -> bool:
        return any(i.tipo == "pocion" for i in self.inventario)

    def usar_pocion(self) -> int:
        for i, item in enumerate(self.inventario):
            if item.tipo == "pocion":
                cantidad = item.efecto.get("curacion", 25)
                self.curar(cantidad)
                self.inventario.pop(i)
                return cantidad
        return 0


def crear_personaje(nombre: str, clase: str, rasgos: list) -> Personaje:
    info = CLASES[clase]
    p = Personaje(
        nombre=nombre,
        clase=clase,
        fuerza=info["fuerza"],
        destreza=info["destreza"],
        inteligencia=info["inteligencia"],
        constitucion=info["constitucion"],
        sabiduria=info["sabiduria"],
        carisma=info["carisma"],
        hp_max=info["hp_base"],
        hp_actual=info["hp_base"],
        mp_max=info["mp_base"],
        mp_actual=info["mp_base"],
        dado_danio=info["dado_danio"],
        armadura=info["armadura_base"],
        rasgos=rasgos,
        habilidad_especial=info["habilidad_especial"],
        habilidad_costo_mp=info["costo_mp"],
    )

    armas_iniciales = {
        "Guerrero": Item("Espada Larga", "arma", "Una espada de acero bien balanceada", 50, {"dado_danio": 8}),
        "Mago": Item("Báculo Arcano", "arma", "Un báculo imbuido de energía mágica", 40, {"dado_danio": 10}),
        "Pícaro": Item("Dagas Gemelas", "arma", "Dos dagas ligeras para ataques rápidos", 35, {"dado_danio": 6}),
        "Clérigo": Item("Maza Sagrada", "arma", "Una maza bendecida por los dioses", 40, {"dado_danio": 6}),
        "Paladín": Item("Espada Bastarda", "arma", "Una espada con inscripciones sagradas", 60, {"dado_danio": 8}),
    }
    arma = armas_iniciales[clase]
    p.inventario.append(arma)
    p.arma_equipada = arma.nombre
    p.inventario.append(
        Item("Poción de Salud", "pocion", "Restaura 25 HP", 15, {"curacion": 25})
    )
    return p
