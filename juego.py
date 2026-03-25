import ui
import guardado
import musica_manager
from personaje import (
    CLASES, PREGUNTAS_PERSONALIDAD, CLASE_RECOMENDADA,
    crear_personaje, Item
)
from historia import ejecutar_escena
from rich.prompt import Confirm


def iniciar():
    # Inicializar música
    musica_manager.inicializar()
    musica_manager.reproducir("menu")

    ui.mostrar_titulo()
    ui.pausa(0.5)

    ui.console.print()
    opcion = ui.elegir_opcion([
        "Nueva Partida",
        "Continuar Partida" if guardado.existe_guardado() else "Continuar (sin partida guardada)",
        "Salir",
    ], titulo="Menú Principal")

    if opcion == 2:
        ui.console.print("\n[dim]Hasta pronto, aventurero.[/dim]\n")
        return

    if opcion == 1:
        if not guardado.existe_guardado():
            ui.console.print("[red]No hay partida guardada.[/red]")
            ui.pausa(1)
            iniciar()
            return
        personaje, estado = guardado.cargar()
        if personaje is None:
            ui.console.print("[red]Error al cargar la partida.[/red]")
            ui.pausa(1)
            iniciar()
            return
        ui.panel_narrativa(
            f"Bienvenido de vuelta, {personaje.nombre}.\n"
            f"Retomas la aventura en la escena: {estado.get('escena_actual', '?')}",
            titulo="Partida Cargada",
            color="green",
        )
        ui.pausa(1)
    else:
        personaje = _crear_personaje()
        estado = {"escena_actual": "1_intro"}

    _bucle_principal(personaje, estado)


def _crear_personaje():
    ui.limpiar()
    ui.separador("gold1", "Creación de Personaje")

    # Nombre
    ui.console.print()
    ui.console.print("[italic dim]¿Cómo se llama el héroe que dará vida a esta historia?[/italic dim]")
    nombre = ui.pedir_nombre()

    # Quiz de personalidad - pantalla propia para el intro
    ui.panel_narrativa(
        "Antes de embarcarte en tu aventura, el Oráculo de Yar desea conocerte. "
        "Responde con honestidad: las respuestas moldearán tu destino.",
        titulo="El Oráculo habla",
    )
    ui.pedir_continuar()

    rasgos = []
    bonus_stats = {}

    # Cada pregunta en su propia pantalla limpia
    total_preguntas = len(PREGUNTAS_PERSONALIDAD)
    for idx, pregunta_data in enumerate(PREGUNTAS_PERSONALIDAD, 1):
        ui.limpiar()
        ui.separador("gold1", f"Pregunta {idx} de {total_preguntas}")
        ui.console.print()
        ui.console.print(f"[bold gold1]{pregunta_data['pregunta']}[/bold gold1]")
        eleccion = ui.elegir_opcion(
            [op[0] for op in pregunta_data["opciones"]],
            titulo="Tu respuesta",
        )
        _, stat, bonus, rasgo = pregunta_data["opciones"][eleccion]
        bonus_stats[stat] = bonus_stats.get(stat, 0) + bonus
        if rasgo not in rasgos:
            rasgos.append(rasgo)

    # Clase recomendada
    stat_dominante = max(bonus_stats, key=bonus_stats.get)
    clase_recomendada = CLASE_RECOMENDADA.get(stat_dominante, "Guerrero")

    # Pantalla: resultado del oráculo
    ui.panel_narrativa(
        f"Tus respuestas revelan un alma {', '.join(rasgos[:3])}.\n\n"
        f"El Oráculo ve en ti un destino de [bold]{clase_recomendada}[/bold].\n"
        f"Tu {stat_dominante} destacará sobre los demás atributos.",
        titulo="El Oráculo habla",
        color="cyan",
    )
    ui.pedir_continuar()

    # Pantalla: elegir clase (se muestra sola, sin nada más)
    nombres_clases = list(CLASES.keys())
    opciones_clases = []
    for nombre_clase, info in CLASES.items():
        recomendado = " [bold green]<- Recomendado[/bold green]" if nombre_clase == clase_recomendada else ""
        opciones_clases.append(f"{nombre_clase} - {info['descripcion']}{recomendado}")

    eleccion_clase = ui.elegir_opcion(opciones_clases, titulo="Elige tu clase")
    clase_elegida = nombres_clases[eleccion_clase]

    # Crear personaje
    personaje = crear_personaje(nombre, clase_elegida, rasgos)

    # Aplicar bonificaciones del quiz
    for stat, valor in bonus_stats.items():
        setattr(personaje, stat, getattr(personaje, stat) + valor)

    # Pantalla: personaje creado (solo el panel narrativo)
    ui.panel_narrativa(
        f"{nombre} el {clase_elegida} ha nacido!\n\n"
        f"{CLASES[clase_elegida]['descripcion']}\n\n"
        f"Habilidad especial: [bold]{personaje.habilidad_especial}[/bold]\n"
        f"- {CLASES[clase_elegida]['desc_habilidad']}",
        titulo="Personaje Creado",
        color=CLASES[clase_elegida]["color"],
    )
    ui.pedir_continuar()

    # Pantalla: stats (se muestra sola)
    ui.mostrar_stats(personaje)
    ui.pedir_continuar("Tu aventura comienza. Presiona Enter...")

    return personaje


def _bucle_principal(personaje, estado):
    escena_actual = estado.get("escena_actual", "1_intro")

    while True:
        # Auto-guardado y música antes de cada escena
        guardado.guardar(personaje, {**estado, "escena_actual": escena_actual})
        musica_manager.reproducir_para_escena(escena_actual)

        siguiente = ejecutar_escena(escena_actual, personaje, estado)

        if siguiente == "fin":
            ui.limpiar()
            ui.mostrar_titulo()
            ui.console.print()
            ui.console.print(Align.center("[bold gold1]Gracias por jugar Eryndor: Tierras Oscuras[/bold gold1]"))
            ui.console.print()
            guardado.borrar_guardado()
            ui.pedir_continuar()
            break
        elif siguiente == "game_over":
            escena_actual = "game_over"
        elif siguiente is None:
            ui.console.print("[red]Error: escena no encontrada.[/red]")
            break
        else:
            escena_actual = siguiente

        estado["escena_actual"] = escena_actual

        # Menú de pausa (solo entre escenas, no en game_over ni fin)
        if escena_actual not in ("game_over", "fin"):
            _comprobar_pausa(personaje, estado)


def _comprobar_pausa(personaje, estado):
    """Permite al jugador ver stats, inventario o equipamiento entre escenas."""
    from rich.prompt import Prompt
    ui.console.print()
    ui.console.print("[dim](S) Estadisticas  (I) Inventario  (E) Equipamiento  (+/-) Volumen  (Enter) Continuar[/dim]")
    respuesta = Prompt.ask("[dim]>[/dim]", default="").strip().lower()
    if respuesta == "s":
        ui.mostrar_stats(personaje)
        ui.pedir_continuar()
    elif respuesta == "i":
        ui.mostrar_inventario(personaje)
        ui.pedir_continuar()
    elif respuesta == "e":
        ui.mostrar_equipamiento(personaje)
    elif respuesta == "+":
        musica_manager.set_volumen(musica_manager.volumen_actual() + 0.1)
        ui.console.print(f"  [yellow]Volumen: {int(musica_manager.volumen_actual() * 100)}%[/yellow]")
    elif respuesta == "-":
        musica_manager.set_volumen(musica_manager.volumen_actual() - 0.1)
        ui.console.print(f"  [yellow]Volumen: {int(musica_manager.volumen_actual() * 100)}%[/yellow]")


# Fix import in juego.py
from rich.align import Align
