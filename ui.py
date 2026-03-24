import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding

console = Console()

TITULO_ASCII = r"""
   ____  _   _  _   _   ____  _____  ___  _   _  ____
  |  _ \| | | || \ | | / ___|| ____|/ _ \| \ | |/ ___|
  | | | | | | ||  \| || |  _ |  _| | | | |  \| |\___ \
  | |_| | |_| || |\  || |_| || |___| |_| | |\  | ___) |
  |____/ \___/ |_| \_| \____||_____|\___/|_| \_||____/

         ___    ____  _____  ____  ____   ____  ___    ___
        ( _ )  |  _ \|  __ ||  _ \|  _ \ / ___|/ _ \  |  _ \  ___
        / _ \  | | | | |__| | |_) | |_) | |   | | | | | | | |/ _ \
       | (_) | | |_| |  _   |  _ <|  __/| |___| |_| | | |_| |  __/
        \___/  |____/|_| |_||_| \_|_|    \____|\___/  |____/ \___|

              E R Y N D O R  —  T i e r r a s  O s c u r a s
"""


def limpiar():
    console.clear()


def pausa(segundos: float = 1.2):
    time.sleep(segundos)


def pausa_corta():
    time.sleep(0.6)


def separador(color: str = "gold1", texto: str = ""):
    if texto:
        console.print(Rule(f"[bold {color}]{texto}[/bold {color}]", style=color))
    else:
        console.print(Rule(style=color))
    pausa_corta()


def mostrar_titulo():
    limpiar()
    console.print()
    console.print(Align.center(Text(TITULO_ASCII, style="bold gold1")))
    console.print()
    console.print(Align.center("[dim italic]Un mundo de magia, peligro y decisiones que importan[/dim italic]"))
    console.print()
    separador("gold1")


def narrar(texto: str, velocidad: float = 0.03, color: str = "white"):
    """Imprime texto letra a letra para efecto dramático."""
    console.print()
    for char in texto:
        console.print(char, end="", style=color)
        time.sleep(velocidad)
    console.print()
    console.print()


def narrar_instantaneo(texto: str, color: str = "white"):
    console.print()
    console.print(f"[{color}]{texto}[/{color}]")
    console.print()


def panel_narrativa(texto: str, titulo: str = "El Dungeon Master habla...", color: str = "gold1", limpiar_antes: bool = True):
    """Panel estilizado para la narrativa del DM. Limpia pantalla por defecto."""
    if limpiar_antes:
        limpiar()
    console.print()
    console.print(Panel(
        f"[italic white]{texto}[/italic white]",
        title=f"[bold {color}]{titulo}[/bold {color}]",
        border_style=color,
        padding=(1, 2),
        box=box.DOUBLE_EDGE,
    ))
    console.print()
    pausa(0.8)


def panel_accion(texto: str, color: str = "cyan"):
    """Panel para acciones del jugador."""
    limpiar()
    console.print(Panel(
        f"[bold {color}]{texto}[/bold {color}]",
        border_style=color,
        padding=(0, 2),
        box=box.ROUNDED,
    ))
    pausa_corta()


def mostrar_stats(personaje):
    from personaje import CLASES
    info_clase = CLASES[personaje.clase]
    color_clase = info_clase["color"]

    limpiar()
    separador(color_clase, f"⚔  {personaje.nombre.upper()}  — Nivel {personaje.nivel} {personaje.clase}")

    # HP y MP barras
    hp_pct = personaje.hp_actual / personaje.hp_max
    mp_pct = personaje.mp_actual / personaje.mp_max
    hp_color = "red" if hp_pct < 0.3 else "yellow" if hp_pct < 0.6 else "green"
    mp_color = "blue"

    hp_barra = _barra(personaje.hp_actual, personaje.hp_max, 20, hp_color)
    mp_barra = _barra(personaje.mp_actual, personaje.mp_max, 20, mp_color)
    xp_barra = _barra(personaje.experiencia, personaje.xp_siguiente_nivel, 20, "magenta")

    tabla_vitales = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    tabla_vitales.add_column(justify="right", style="dim white", width=10)
    tabla_vitales.add_column(width=30)
    tabla_vitales.add_column(justify="right", style="dim white")

    tabla_vitales.add_row(
        "[bold red]❤  HP[/bold red]", hp_barra,
        f"[{hp_color}]{personaje.hp_actual}[/{hp_color}][dim]/{personaje.hp_max}[/dim]"
    )
    tabla_vitales.add_row(
        "[bold blue]✦  MP[/bold blue]", mp_barra,
        f"[{mp_color}]{personaje.mp_actual}[/{mp_color}][dim]/{personaje.mp_max}[/dim]"
    )
    tabla_vitales.add_row(
        "[bold magenta]★  XP[/bold magenta]", xp_barra,
        f"[magenta]{personaje.experiencia}[/magenta][dim]/{personaje.xp_siguiente_nivel}[/dim]"
    )
    console.print(tabla_vitales)
    console.print()

    # Stats de atributos
    tabla_stats = Table(box=box.SIMPLE_HEAVY, show_header=True, padding=(0, 2))
    tabla_stats.add_column("Atributo", style="bold dim white", width=14)
    tabla_stats.add_column("Valor", justify="center", width=8)
    tabla_stats.add_column("Mod", justify="center", width=8)

    stats_data = [
        ("Fuerza", personaje.fuerza, personaje.mod_fuerza, "red"),
        ("Destreza", personaje.destreza, personaje.mod_destreza, "green"),
        ("Inteligencia", personaje.inteligencia, personaje.mod_inteligencia, "blue"),
        ("Constitución", personaje.constitucion, personaje.mod_constitucion, "orange3"),
        ("Sabiduría", personaje.sabiduria, personaje.mod_sabiduria, "yellow"),
        ("Carisma", personaje.carisma, personaje.mod_carisma, "magenta"),
    ]
    for nombre, valor, mod, color in stats_data:
        mod_str = f"[green]+{mod}[/green]" if mod >= 0 else f"[red]{mod}[/red]"
        tabla_stats.add_row(
            f"[{color}]{nombre}[/{color}]",
            f"[bold white]{valor}[/bold white]",
            mod_str,
        )
    console.print(tabla_stats)

    # Info adicional
    console.print()
    console.print(
        f"  [gold1]Oro:[/gold1] [yellow]{personaje.oro} monedas[/yellow]   "
        f"[gold1]Habilidad:[/gold1] [{color_clase}]{personaje.habilidad_especial}[/{color_clase}] "
        f"([dim]{personaje.habilidad_usos} usos[/dim])   "
        f"[gold1]Armadura:[/gold1] {personaje.armadura}"
    )

    if personaje.rasgos:
        rasgos_str = ", ".join(personaje.rasgos)
        console.print(f"  [gold1]Rasgos:[/gold1] [italic dim]{rasgos_str}[/italic dim]")

    console.print()
    separador(color_clase)


def mostrar_estado_combate(personaje, enemigo):
    limpiar()
    separador("red", "⚔  COMBATE")

    # Panel del enemigo
    hp_e_pct = enemigo.hp_actual / enemigo.hp_max
    hp_e_color = "red" if hp_e_pct < 0.3 else "yellow" if hp_e_pct < 0.6 else "green"
    barra_e = _barra(enemigo.hp_actual, enemigo.hp_max, 22, hp_e_color)

    panel_enemigo = Panel(
        f"[bold red]{enemigo.icono} {enemigo.nombre}[/bold red]\n"
        f"[dim italic]{enemigo.descripcion}[/dim italic]\n\n"
        f"[bold red]❤ HP:[/bold red] {barra_e} [{hp_e_color}]{enemigo.hp_actual}[/{hp_e_color}][dim]/{enemigo.hp_max}[/dim]",
        border_style="red",
        box=box.HEAVY,
        padding=(0, 1),
    )

    # Panel del jugador
    hp_j_pct = personaje.hp_actual / personaje.hp_max
    hp_j_color = "red" if hp_j_pct < 0.3 else "yellow" if hp_j_pct < 0.6 else "green"
    barra_j = _barra(personaje.hp_actual, personaje.hp_max, 22, hp_j_color)
    barra_mp_j = _barra(personaje.mp_actual, personaje.mp_max, 22, "blue")

    from personaje import CLASES
    color_clase = CLASES[personaje.clase]["color"]

    panel_jugador = Panel(
        f"[bold {color_clase}]{CLASES[personaje.clase]['icono']} {personaje.nombre}[/bold {color_clase}] [dim](Nv. {personaje.nivel} {personaje.clase})[/dim]\n\n"
        f"[bold red]❤ HP:[/bold red] {barra_j} [{hp_j_color}]{personaje.hp_actual}[/{hp_j_color}][dim]/{personaje.hp_max}[/dim]\n"
        f"[bold blue]✦ MP:[/bold blue] {barra_mp_j} [blue]{personaje.mp_actual}[/blue][dim]/{personaje.mp_max}[/dim]",
        border_style=color_clase,
        box=box.HEAVY,
        padding=(0, 1),
    )

    console.print(Columns([panel_enemigo, panel_jugador], equal=True))
    console.print()


def menu_acciones_combate(personaje) -> str:
    from personaje import CLASES
    info = CLASES[personaje.clase]

    opciones = [
        f"[bold white]1.[/bold white] [red]⚔ Atacar[/red]",
        f"[bold white]2.[/bold white] [{info['color']}]✦ {personaje.habilidad_especial}[/{info['color']}]"
        + (f" [dim]({personaje.habilidad_usos} usos)[/dim]" if personaje.habilidad_usos > 0 else " [dim red](sin usos)[/dim red]"),
        f"[bold white]3.[/bold white] [green]⊕ Usar Poción[/green]"
        + (" [dim](tienes 1+)[/dim]" if personaje.tiene_pocion() else " [dim red](no tienes)[/dim red]"),
        f"[bold white]4.[/bold white] [yellow]↩ Huir[/yellow]",
    ]

    tabla = Table(box=box.ROUNDED, show_header=False, padding=(0, 2), border_style="dim white")
    tabla.add_column()
    for op in opciones:
        tabla.add_row(op)

    console.print(Panel(tabla, title="[bold white]¿Qué haces?[/bold white]", border_style="dim white", box=box.ROUNDED))
    console.print()

    while True:
        eleccion = Prompt.ask("[bold white]>[/bold white]", choices=["1", "2", "3", "4"])
        return eleccion


def mostrar_resultado_ataque(ataque: dict, danio: dict = None, nombre_atacante: str = ""):
    """Muestra el resultado de un ataque en un panel limpio."""
    if ataque["critico"]:
        resultado_txt = "[bold gold1]GOLPE CRITICO[/bold gold1]"
        borde = "gold1"
    elif ataque["pifia"]:
        resultado_txt = "[bold red]PIFIA[/bold red]"
        borde = "red"
    elif ataque["impacto"]:
        resultado_txt = "[bold green]IMPACTO[/bold green]"
        borde = "green"
    else:
        resultado_txt = "[bold red]FALLO[/bold red]"
        borde = "red"

    # Construir contenido del panel
    lineas = [f"[dim]{nombre_atacante} tira el dado...[/dim]\n"]
    lineas.append(f"  Dado:  [bold yellow]{ataque['dado']}[/bold yellow] de 20")
    lineas.append(f"  Resultado:  {resultado_txt}")

    if ataque["impacto"] and danio:
        if ataque["critico"]:
            lineas.append(f"\n  [bold red]Dano: {danio['total']} (critico)[/bold red]")
        else:
            lineas.append(f"\n  [red]Dano: {danio['total']}[/red]")
    elif ataque["pifia"]:
        lineas.append(f"\n  [dim red]Tropieza y falla estrepitosamente.[/dim red]")

    console.print(Panel(
        "\n".join(lineas),
        title="[bold white]Ataque[/bold white]",
        border_style=borde,
        padding=(1, 2),
        box=box.ROUNDED,
    ))
    pausa(1.0)


def mostrar_resultado_chequeo(chequeo: dict, nombre_stat: str, dificultad: int):
    """Muestra un chequeo de habilidad en un panel limpio y legible."""
    limpiar()

    if chequeo["critico_exito"]:
        resultado_txt = "[bold gold1]EXITO CRITICO[/bold gold1]"
        borde = "gold1"
        emoji = ">>>"
    elif chequeo["critico_fallo"]:
        resultado_txt = "[bold red]FALLO CRITICO[/bold red]"
        borde = "red"
        emoji = "!!!"
    elif chequeo["exito"]:
        resultado_txt = "[bold green]EXITO[/bold green]"
        borde = "green"
        emoji = ">>>"
    else:
        resultado_txt = "[bold red]FALLO[/bold red]"
        borde = "red"
        emoji = "---"

    mod_str = f"+{chequeo['modificador']}" if chequeo["modificador"] >= 0 else str(chequeo["modificador"])

    contenido = (
        f"[dim]Tirando el dado de {nombre_stat}...[/dim]\n\n"
        f"  Dado:        [bold yellow]{chequeo['dado']}[/bold yellow] de 20\n"
        f"  Modificador: [cyan]{mod_str}[/cyan]\n"
        f"  Total:       [bold white]{chequeo['total']}[/bold white]\n"
        f"  Dificultad:  [dim]{dificultad}[/dim]\n\n"
        f"  {emoji}  {resultado_txt}  {emoji}"
    )

    console.print()
    console.print(Panel(
        contenido,
        title=f"[bold yellow]Chequeo de {nombre_stat}[/bold yellow]",
        border_style=borde,
        padding=(1, 3),
        box=box.DOUBLE_EDGE,
    ))
    console.print()
    pausa(1.2)


def mostrar_subida_nivel(personaje):
    limpiar()
    separador("gold1", "★  NIVEL SUPERIOR  ★")
    console.print()
    console.print(Align.center(f"[bold gold1]¡{personaje.nombre} alcanza el Nivel {personaje.nivel}![/bold gold1]"))
    console.print()
    for _ in range(3):
        console.print(Align.center("[bold yellow]✦ ✦ ✦[/bold yellow]"))
        time.sleep(0.3)
    console.print()
    console.print(f"  [green]HP máximo aumentado[/green]")
    console.print(f"  [blue]MP máximo aumentado[/blue]")
    console.print(f"  [yellow]Estadísticas mejoradas[/yellow]")
    console.print(f"  [cyan]Habilidad especial restaurada (3 usos)[/cyan]")
    console.print()
    separador("gold1")
    pausa(1.0)


def mostrar_recompensa(xp: int, oro: int, item=None):
    limpiar()
    separador("gold1", "Recompensa")
    console.print(f"  [magenta]+{xp} Experiencia[/magenta]")
    if oro > 0:
        console.print(f"  [yellow]+{oro} Monedas de Oro[/yellow]")
    if item:
        console.print(f"  [cyan]Objeto encontrado: {item.nombre}[/cyan]  [dim]{item.descripcion}[/dim]")
    console.print()
    pausa(0.8)


def mostrar_inventario(personaje):
    limpiar()
    separador("yellow", "Inventario")
    if not personaje.inventario:
        console.print("[dim]  El inventario está vacío.[/dim]")
    else:
        tabla = Table(box=box.SIMPLE, show_header=True, padding=(0, 1))
        tabla.add_column("Objeto", style="white", width=22)
        tabla.add_column("Tipo", style="dim", width=10)
        tabla.add_column("Descripción", style="dim italic", width=40)
        for item in personaje.inventario:
            color = {"arma": "red", "pocion": "green", "magico": "cyan", "armadura": "blue"}.get(item.tipo, "white")
            tabla.add_row(f"[{color}]{item.nombre}[/{color}]", item.tipo, item.descripcion)
        console.print(tabla)
    console.print(f"  [yellow]Oro:[/yellow] {personaje.oro} monedas")
    console.print()


def elegir_opcion(opciones: list, titulo: str = "¿Qué decides hacer?") -> int:
    """Muestra un menú y retorna el índice elegido (0-based)."""
    console.print()
    tabla = Table(box=box.ROUNDED, show_header=False, padding=(0, 2), border_style="gold1")
    tabla.add_column(width=60)
    for i, op in enumerate(opciones, 1):
        tabla.add_row(f"[bold gold1]{i}.[/bold gold1] [white]{op}[/white]")

    console.print(Panel(tabla, title=f"[bold gold1]{titulo}[/bold gold1]", border_style="gold1", box=box.DOUBLE_EDGE))
    console.print()

    choices = [str(i) for i in range(1, len(opciones) + 1)]
    while True:
        eleccion = Prompt.ask("[bold gold1]>[/bold gold1]", choices=choices)
        return int(eleccion) - 1


def pedir_nombre() -> str:
    console.print()
    nombre = Prompt.ask("[bold gold1]Escribe el nombre de tu héroe[/bold gold1]")
    return nombre.strip() or "Aventurero"


def pedir_continuar(mensaje: str = "Presiona Enter para continuar..."):
    console.print(f"\n[dim]{mensaje}[/dim]")
    input()
    limpiar()


def _barra(actual: int, maximo: int, largo: int, color: str) -> str:
    if maximo == 0:
        pct = 0
    else:
        pct = max(0, min(1, actual / maximo))
    llenas = int(pct * largo)
    vacias = largo - llenas
    barra = f"[{color}]{'█' * llenas}[/{color}][dim]{'░' * vacias}[/dim]"
    return barra
