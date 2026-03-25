from dataclasses import dataclass, field
import random


@dataclass
class Enemigo:
    nombre: str
    descripcion: str
    hp_max: int
    hp_actual: int
    bonus_ataque: int
    armadura: int
    dado_danio: int
    mod_danio: int
    xp: int
    oro_min: int
    oro_max: int
    icono: str = "[red]✦[/red]"
    habilidad_especial: str = ""
    habilidad_chance: float = 0.0
    danio_habilidad: int = 0
    fase_2: bool = False
    regenera: int = 0
    es_boss: bool = False
    # Partes del cuerpo: {nombre: {armadura_mod, danio_mult, efecto, descripcion}}
    partes_cuerpo: dict = field(default_factory=dict)

    def esta_vivo(self) -> bool:
        return self.hp_actual > 0

    def recibir_danio(self, cantidad: int):
        self.hp_actual = max(0, self.hp_actual - cantidad)

    def oro_al_morir(self) -> int:
        return random.randint(self.oro_min, self.oro_max)

    def usar_habilidad_especial(self) -> bool:
        return self.habilidad_especial != "" and random.random() < self.habilidad_chance


def crear_enemigo(tipo: str) -> Enemigo:
    plantillas = {
        # Arco 1
        "cultista": Enemigo(
            nombre="Cultista del Umbral",
            descripcion="Un fanático de ojos inyectados en sangre que murmura rezos oscuros.",
            hp_max=25, hp_actual=25,
            bonus_ataque=3, armadura=11,
            dado_danio=6, mod_danio=1,
            xp=60, oro_min=5, oro_max=18,
            icono="[red]✦[/red]",
        ),
        "lider_cultistas": Enemigo(
            nombre="Sacerdote del Umbral",
            descripcion="Viste túnicas negras con runas carmesí. Sus ojos brillan con poder oscuro.",
            hp_max=42, hp_actual=42,
            bonus_ataque=5, armadura=13,
            dado_danio=8, mod_danio=2,
            xp=120, oro_min=15, oro_max=35,
            icono="[red]✦[/red]",
            habilidad_especial="Maldición Sombría",
            habilidad_chance=0.30,
            danio_habilidad=12,
        ),
        # Arco 2
        "esqueleto": Enemigo(
            nombre="Esqueleto Guerrero",
            descripcion="Huesos blancos que se mueven solos, empuñando una espada mohosa.",
            hp_max=30, hp_actual=30,
            bonus_ataque=4, armadura=12,
            dado_danio=6, mod_danio=1,
            xp=80, oro_min=0, oro_max=5,
            icono="[dim white]✦[/dim white]",
        ),
        "espectro": Enemigo(
            nombre="Espectro Guardián",
            descripcion="Una figura etérea que flota en la oscuridad. Su toque hiela hasta el alma.",
            hp_max=50, hp_actual=50,
            bonus_ataque=6, armadura=13,
            dado_danio=8, mod_danio=3,
            xp=150, oro_min=0, oro_max=10,
            icono="[cyan]✦[/cyan]",
            habilidad_especial="Toque Helado",
            habilidad_chance=0.35,
            danio_habilidad=15,
        ),
        # Arco 3
        "golem_obsidiana": Enemigo(
            nombre="Gólem de Obsidiana",
            descripcion="Una colosal figura de piedra negra volcánica. Cada paso hace temblar el suelo.",
            hp_max=80, hp_actual=80,
            bonus_ataque=7, armadura=17,
            dado_danio=10, mod_danio=4,
            xp=250, oro_min=0, oro_max=0,
            icono="[dark_goldenrod]✦[/dark_goldenrod]",
            habilidad_especial="Puño Sísmico",
            habilidad_chance=0.25,
            danio_habilidad=20,
            es_boss=True,
            partes_cuerpo={
                "Cuerpo": {"armadura_mod": 0, "danio_mult": 1.0, "desc": "Ataque normal al torso"},
                "Cabeza": {"armadura_mod": 3, "danio_mult": 1.5, "desc": "Mas dificil, mas dano"},
                "Cristales Oculares": {"armadura_mod": 5, "danio_mult": 1.0, "desc": "Punto debil: reduce su armadura", "efecto": "reducir_armadura"},
            },
        ),
        # Arco 4
        "vampiro": Enemigo(
            nombre="Conde Valdris",
            descripcion="Un vampiro antiguo de porte aristocrático. Sus ojos rojos destilan siglos de crueldad.",
            hp_max=70, hp_actual=70,
            bonus_ataque=8, armadura=15,
            dado_danio=10, mod_danio=3,
            xp=300, oro_min=40, oro_max=80,
            icono="[magenta]✦[/magenta]",
            habilidad_especial="Drenaje Vital",
            habilidad_chance=0.35,
            danio_habilidad=18,
            regenera=5,
        ),
        # Arco 5 - Jefe final
        "malachar": Enemigo(
            nombre="Malachar, el Lich Eterno",
            descripcion="Una figura esquelética envuelta en túnicas negras y energía de muerte. Sus ojos son dos llamas violetas.",
            hp_max=120, hp_actual=120,
            bonus_ataque=10, armadura=16,
            dado_danio=12, mod_danio=5,
            xp=800, oro_min=100, oro_max=200,
            icono="[bright_magenta]✦[/bright_magenta]",
            habilidad_especial="Rayo de Muerte",
            habilidad_chance=0.35,
            danio_habilidad=28,
            fase_2=True,
            regenera=8,
            es_boss=True,
            partes_cuerpo={
                "Cuerpo": {"armadura_mod": 0, "danio_mult": 1.0, "desc": "Ataque normal"},
                "Cabeza": {"armadura_mod": 4, "danio_mult": 1.5, "desc": "Mas dificil, mas dano"},
                "Filacteria (Collar)": {"armadura_mod": 6, "danio_mult": 1.0, "desc": "Destruye su regeneracion", "efecto": "destruir_filacteria"},
                "Manos": {"armadura_mod": 2, "danio_mult": 0.8, "desc": "Reduce su ataque", "efecto": "reducir_ataque"},
            },
        ),
    }
    return plantillas[tipo]
