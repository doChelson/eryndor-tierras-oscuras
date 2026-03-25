import random
from dados import tirada_ataque, tirada_danio, chequeo_habilidad
import ui


def iniciar_combate(personaje, enemigo) -> dict:
    """
    Maneja un combate completo.
    Retorna: {"victoria": bool, "huyo": bool, "xp": int, "oro": int}
    """
    turno = 1
    en_fase_2 = False

    while personaje.esta_vivo() and enemigo.esta_vivo():
        ui.mostrar_estado_combate(personaje, enemigo)

        # Fase 2 del jefe final
        if enemigo.fase_2 and not en_fase_2 and enemigo.hp_actual <= enemigo.hp_max // 2:
            en_fase_2 = True
            ui.panel_narrativa(
                f"¡{enemigo.nombre} ruge de rabia! Su poder se multiplica. "
                f"Las llamas violetas en sus ojos se intensifican y una energía oscura lo envuelve.",
                titulo="¡FASE 2!",
                color="bright_magenta",
            )
            enemigo.bonus_ataque += 2
            enemigo.habilidad_chance += 0.15

        # Regeneración del enemigo
        if enemigo.regenera > 0 and turno > 1:
            enemigo.hp_actual = min(enemigo.hp_max, enemigo.hp_actual + enemigo.regenera)
            ui.console.print(f"[dim red]{enemigo.nombre} se regenera {enemigo.regenera} HP.[/dim red]")

        # Turno del jugador
        resultado_jugador = _turno_jugador(personaje, enemigo)
        if resultado_jugador == "huyo":
            return {"victoria": False, "huyo": True, "xp": 0, "oro": 0}

        if not enemigo.esta_vivo():
            break

        # Turno del enemigo
        _turno_enemigo(personaje, enemigo)

        turno += 1

    if not personaje.esta_vivo():
        return {"victoria": False, "huyo": False, "xp": 0, "oro": 0}

    # Victoria
    xp = enemigo.xp
    oro = enemigo.oro_al_morir()
    subio = personaje.agregar_xp(xp)
    personaje.oro += oro
    personaje.enemigos_derrotados += 1

    ui.panel_narrativa(
        f"¡{enemigo.nombre} cae derrotado! Su último grito resuena en el aire y luego... silencio.",
        titulo="✦ Victoria ✦",
        color="gold1",
    )
    ui.mostrar_recompensa(xp, oro)

    if subio:
        ui.mostrar_subida_nivel(personaje)

    return {"victoria": True, "huyo": False, "xp": xp, "oro": oro}


def _turno_jugador(personaje, enemigo) -> str:
    """Retorna 'atacar', 'habilidad', 'pocion' o 'huyo'."""
    eleccion = ui.menu_acciones_combate(personaje)

    if eleccion == "1":
        _ataque_jugador(personaje, enemigo)
    elif eleccion == "2":
        _usar_habilidad(personaje, enemigo)
    elif eleccion == "3":
        _usar_pocion(personaje)
    elif eleccion == "4":
        return _intentar_huida(personaje, enemigo)

    return "ok"


def _ataque_jugador(personaje, enemigo):
    stat_ataque = max(personaje.fuerza, personaje.destreza)
    mod = (stat_ataque - 10) // 2

    # Si es boss, elegir parte del cuerpo
    parte = None
    armadura_objetivo = enemigo.armadura
    mult_danio = 1.0
    if enemigo.es_boss and enemigo.partes_cuerpo:
        parte = ui.elegir_parte_cuerpo(enemigo)
        armadura_objetivo = enemigo.armadura + parte.get("armadura_mod", 0)
        mult_danio = parte.get("danio_mult", 1.0)

    ataque = tirada_ataque(mod, armadura_objetivo)
    danio = None
    if ataque["impacto"]:
        danio = tirada_danio(personaje.dado_danio, mod, critico=ataque["critico"])
        danio_final = int(danio["total"] * mult_danio)
        danio["total"] = max(1, danio_final)
        enemigo.recibir_danio(danio["total"])

        # Aplicar efecto de la parte del cuerpo
        if parte and "efecto" in parte:
            _aplicar_efecto_parte(parte, enemigo)

    ui.mostrar_resultado_ataque(ataque, danio, personaje.nombre)
    if danio:
        ui.console.print(f"  [red]{enemigo.nombre}: HP {enemigo.hp_actual}/{enemigo.hp_max}[/red]")
    ui.pausa_corta()


def _aplicar_efecto_parte(parte, enemigo):
    efecto = parte["efecto"]
    if efecto == "destruir_filacteria":
        enemigo.regenera = 0
        enemigo.fase_2 = False
        ui.panel_narrativa(
            f"La filacteria se resquebraja! El cristal negro estalla en mil pedazos.\n\n"
            f"{enemigo.nombre} ruge de dolor. Ya no puede regenerarse!",
            titulo="Filacteria Destruida!",
            color="gold1",
        )
    elif efecto == "reducir_armadura":
        enemigo.armadura = max(8, enemigo.armadura - 3)
        ui.console.print(f"  [green]Su armadura se debilita! (Armadura: {enemigo.armadura})[/green]")
    elif efecto == "reducir_ataque":
        enemigo.bonus_ataque = max(1, enemigo.bonus_ataque - 2)
        ui.console.print(f"  [green]Sus ataques se debilitan! (Ataque: +{enemigo.bonus_ataque})[/green]")


def _usar_habilidad(personaje, enemigo):
    from personaje import CLASES
    info = CLASES[personaje.clase]

    if personaje.habilidad_usos <= 0:
        ui.console.print("[dim red]Ya no tienes usos de habilidad.[/dim red]")
        _ataque_jugador(personaje, enemigo)
        return

    if personaje.habilidad_costo_mp > 0 and not personaje.usar_mp(personaje.habilidad_costo_mp):
        ui.console.print(f"[dim red]No tienes suficiente MP para {personaje.habilidad_especial}.[/dim red]")
        _ataque_jugador(personaje, enemigo)
        return

    personaje.habilidad_usos -= 1
    habilidad = personaje.habilidad_especial
    mod = (max(personaje.fuerza, personaje.destreza, personaje.inteligencia) - 10) // 2

    ui.panel_accion(f"✦ {personaje.nombre} usa {habilidad}!", color=info["color"])

    if habilidad == "Golpe Poderoso":
        ataque = tirada_ataque(mod + 2, enemigo.armadura)
        if ataque["impacto"]:
            danio = tirada_danio(personaje.dado_danio * 2, mod)
            enemigo.recibir_danio(danio["total"])
            ui.console.print(f"  [red]¡Golpe poderoso! {danio['total']} de daño.[/red]")
        else:
            ui.console.print("[dim]El golpe falla.[/dim]")

    elif habilidad == "Bola de Fuego":
        from dados import tirar_dados
        dados = tirar_dados(10, 2)
        mod_int = personaje.mod_inteligencia
        danio_total = max(1, sum(dados) + mod_int)
        ui.console.print(f"  [bold red]¡Bola de Fuego! {danio_total} de daño arcano.[/bold red]")
        enemigo.recibir_danio(danio_total)

    elif habilidad == "Ataque Furtivo":
        ataque = tirada_ataque(mod + 3, enemigo.armadura)
        if ataque["impacto"]:
            danio = tirada_danio(personaje.dado_danio, mod)
            danio_triple = danio["total"] * 3
            enemigo.recibir_danio(danio_triple)
            ui.console.print(f"  [green]¡Golpe furtivo! {danio_triple} de daño.[/green]")
        else:
            ui.console.print("[dim]El ataque furtivo falla.[/dim]")

    elif habilidad == "Sanación Divina":
        from dados import tirar_dados
        dados = tirar_dados(8, 2)
        curacion = max(1, sum(dados) + personaje.mod_sabiduria)
        personaje.curar(curacion)
        ui.console.print(f"  [bold green]¡Sanación Divina! Recuperas {curacion} HP.[/bold green]")

    elif habilidad == "Smite Sagrado":
        ataque = tirada_ataque(mod, enemigo.armadura)
        if ataque["impacto"]:
            from dados import tirar_dados
            danio_sagrado = tirar_dados(8, 2)
            danio_base = tirada_danio(personaje.dado_danio, mod)
            danio_total = danio_base["total"] + sum(danio_sagrado)
            enemigo.recibir_danio(danio_total)
            ui.console.print(f"  [bold yellow]¡Smite Sagrado! {danio_total} de daño divino.[/bold yellow]")
        else:
            ui.console.print("[dim]El smite falla.[/dim]")

    ui.console.print(f"  [dim](HP {enemigo.nombre}: {enemigo.hp_actual}/{enemigo.hp_max})[/dim]")
    ui.pausa_corta()


def _usar_pocion(personaje):
    if not personaje.tiene_pocion():
        ui.panel_narrativa("No tienes pociones disponibles.", titulo="Sin Pociones", color="red")
        return
    cantidad = personaje.usar_pocion()
    ui.panel_narrativa(
        f"Bebes una poción y recuperas [bold green]{cantidad} HP[/bold green].\n\n"
        f"HP: {personaje.hp_actual}/{personaje.hp_max}",
        titulo="Pocion Utilizada",
        color="green",
    )


def _intentar_huida(personaje, enemigo) -> str:
    check = chequeo_habilidad(personaje.destreza, 13)
    ui.mostrar_resultado_chequeo(check, "Destreza", 13)
    if check["exito"]:
        ui.panel_narrativa(
            "Consigues escapar entre las sombras!",
            titulo="Huida Exitosa",
            color="yellow",
        )
        return "huyo"
    else:
        ui.panel_narrativa(
            "No puedes escapar! El enemigo te corta el paso.",
            titulo="Huida Fallida",
            color="red",
        )
        return "ok"


def _turno_enemigo(personaje, enemigo):
    # ¿Usa habilidad especial?
    if enemigo.usar_habilidad_especial():
        danio = max(5, enemigo.danio_habilidad + random.randint(-3, 3))
        personaje.recibir_danio(danio)
        ui.panel_narrativa(
            f"{enemigo.nombre} usa [bold red]{enemigo.habilidad_especial}[/bold red]!\n\n"
            f"Recibes [bold red]{danio}[/bold red] de daño.\n"
            f"Tu HP: {personaje.hp_actual}/{personaje.hp_max}",
            titulo=f"Turno de {enemigo.nombre}",
            color="red",
        )
    else:
        ataque = tirada_ataque(enemigo.bonus_ataque, personaje.armadura)
        danio = None
        if ataque["impacto"]:
            mod_e = enemigo.bonus_ataque // 2
            danio = tirada_danio(enemigo.dado_danio, mod_e, critico=ataque["critico"])
            personaje.recibir_danio(danio["total"])

        ui.mostrar_resultado_ataque(ataque, danio, enemigo.nombre)
        if danio:
            ui.console.print(f"  [red]Tu HP: {personaje.hp_actual}/{personaje.hp_max}[/red]")

    if not personaje.esta_vivo():
        ui.console.print(f"\n[bold red]Has caído en batalla...[/bold red]")
    ui.pausa(1.0)
