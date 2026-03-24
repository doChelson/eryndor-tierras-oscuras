"""
Historia: Eryndor — Tierras Oscuras
Arcos: 3 (jugables) de 5 (planificados)
Arco 1: El Llamado de Rocabruna
Arco 2: Las Ruinas de Yar
Arco 3: La Torre de Malachar
"""

import ui
import combate
from dados import chequeo_habilidad, tirar_dado
from enemigos import crear_enemigo
from personaje import Item

# Registro de escenas
ESCENAS = {}


def escena(id_escena):
    def decorator(func):
        ESCENAS[id_escena] = func
        return func
    return decorator


def ejecutar_escena(id_escena, personaje, estado):
    if id_escena not in ESCENAS:
        return "fin"
    return ESCENAS[id_escena](personaje, estado)


# ==============================================================================
#  ARCO 1: EL LLAMADO DE ROCABRUNA
# ==============================================================================

@escena("1_intro")
def escena_1_intro(personaje, estado):
    ui.limpiar()
    ui.separador("gold1", "ARCO I — El Llamado de Rocabruna")
    ui.panel_narrativa(
        "El mundo de Eryndor lleva siglos bajo la sombra de una profecía olvidada, "
        "escrita por el sabio Marcelo el Vidente, primer héroe de Eryndor:\n\n"
        "\"Cuando las estrellas se apaguen sobre las Ruinas de Yar, el Lich Eterno "
        "despertará al Dios del Caos, y la oscuridad devorará todos los reinos.\"\n\n"
        "Nadie le prestó atención. Hasta ahora.",
        titulo="Prólogo",
        color="dim white",
    )
    ui.pedir_continuar()

    ui.limpiar()
    ui.panel_narrativa(
        f"Eres {personaje.nombre}, {personaje.clase.lower()} de Eryndor. "
        f"Llevas semanas viajando por caminos polvorientos cuando el olor a humo te guía "
        f"hasta la aldea de Rocabruna.\n\n"
        f"Lo que ves te hiela la sangre. La mitad del pueblo está en llamas. "
        f"Aldeanos huyen despavoridos. Y entre el caos, hombres con túnicas negras "
        f"y runas carmesí graban símbolos en las paredes.",
        titulo="La Aldea de Rocabruna",
    )
    ui.pedir_continuar()
    return "1_aldea"


@escena("1_aldea")
def escena_1_aldea(personaje, estado):
    ui.limpiar()
    ui.panel_narrativa(
        "Una anciana llamada Martha te agarra del brazo entre el humo y el caos. "
        "Es la curandera del pueblo, conocida por todos. "
        "Sus ojos están llenos de lágrimas pero su voz es firme:\n\n"
        "\"¡Forastero! ¡Gracias a los dioses que pasabas por aquí! "
        "Estos... estos monstruos dicen servir a alguien llamado Malachar. "
        "Se llevan a los jóvenes. Mi nieto... mi nieto está allá adentro.\"\n\n"
        "Señala hacia la herrería en llamas. Un guardia llamado Peter intenta apagar el fuego "
        "solo con un balde, pero es inútil. Escuchas un grito infantil entre las llamas.",
    )

    eleccion = ui.elegir_opcion([
        "Entrar corriendo a la herrería para rescatar al niño.",
        "Buscar al anciano del pueblo para entender qué ocurre.",
        "Atacar a los cultistas más cercanos antes de hacer nada.",
    ])

    if eleccion == 0:
        ui.panel_accion("Te lanzas hacia la herrería sin dudar.", color="red")
        check = chequeo_habilidad(personaje.constitucion, 12)
        ui.mostrar_resultado_chequeo(check, "Constitución", 12)
        if check["exito"]:
            ui.panel_narrativa(
                "El calor es sofocante pero aguantas. Entre las vigas ardientes encuentras "
                "a un niño de ocho años acurrucado detrás de un yunque. Lo cargas en brazos "
                "y salís al exterior tosiendo y con el pelo chamuscado.\n\n"
                "Martha llora de alegría. \"¡Aldric! ¡Gracias a los dioses!\"\n\n"
                "Peter, el guardia, te da una palmada en la espalda. \"Más valiente que todos nosotros.\"\n"
                "El pueblo entero te vio. Los ojos de los aldeanos brillan de gratitud y esperanza.",
                titulo="✦ Acción Heroica",
                color="green",
            )
            personaje.decisiones_heroicas += 1
            personaje.agregar_xp(40)
            personaje.flags["salvo_nino"] = True
        else:
            ui.panel_narrativa(
                "El humo te ciega. Una viga cae y te golpea el hombro. "
                "Con esfuerzo logras sacar al niño, pero sales con quemaduras y magullado.\n\n"
                "Martha te abraza llorando. Valió la pena.",
                titulo="Éxito Costoso",
                color="yellow",
            )
            personaje.recibir_danio(10)
            personaje.flags["salvo_nino"] = True
            personaje.agregar_xp(30)

    elif eleccion == 1:
        ui.panel_narrativa(
            "Encuentras al anciano alcalde, Tobias, escondido detrás del pozo central. "
            "Con voz temblorosa te explica:\n\n"
            "\"El Culto del Umbral... llevan semanas apareciendo. Buscan algo en las Ruinas "
            "de Yar, al norte del Bosque Umbrío. Dicen que su maestro Malachar necesita "
            "un artefacto para \"abrir el portal eterno\". Esto es malo, muy malo.\"\n\n"
            "Te da un mapa tosco con el camino al bosque y 10 monedas de oro.",
            titulo="Información Valiosa",
        )
        personaje.oro += 10
        personaje.flags["tiene_mapa"] = True
        personaje.agregar_xp(20)

    else:
        ui.panel_accion("Desenvuelves tu arma y te lanzas contra los cultistas.", color="red")
        ui.panel_narrativa(
            "Derrotas a dos cultistas en combate rápido. Los demás huyen a las sombras. "
            "Los aldeanos gritan de alivio. Pero un cultista te lanza una maldición al huir:\n\n"
            "\"¡Necio! No puedes detener la voluntad de Malachar. Las Ruinas de Yar caerán "
            "y el Lich Eterno despertará al dios dormido. ¡Lo verás!\"\n\n"
            "Antes de que puedas alcanzarlo, desaparece entre las sombras.",
            titulo="Combate en las Calles",
            color="red",
        )
        personaje.decisiones_heroicas += 1
        personaje.agregar_xp(35)

    ui.pedir_continuar()
    return "1_mision"


@escena("1_mision")
def escena_1_mision(personaje, estado):
    ui.limpiar()
    ui.panel_narrativa(
        "El anciano alcalde Tobias te reúne con los líderes del pueblo. "
        "En la taberna La Herradura Dorada —regentada por Facundo, un tabernero corpulento "
        "con una cicatriz en la ceja y el corazón más grande de Eryndor— te explica:\n\n"
        "\"Las Ruinas de Yar fueron un gran templo hace mil años. Se dice que en su interior "
        "descansa el Artefacto del Umbral: una reliquia capaz de abrir un portal entre "
        "el mundo de los vivos y el reino de la muerte.\n\n"
        "Si Malachar lo obtiene... bueno, la profecía de Marcelo dice que nadie podrá detenerlo.\n\n"
        "Tú eres la única persona capaz de llegar allí. Te pido que vayas. "
        "El pueblo de Rocabruna no tiene más héroes que tú esta noche.\"\n\n"
        "Facundo te pone una jarra de hidromiel en la mano. \"Bebe, que el camino es largo.\"",
        titulo="La Misión",
    )

    ui.pedir_continuar()
    ui.panel_narrativa(
        "Antes de partir, los aldeanos te ofrecen lo poco que tienen. "
        "Martha, la curandera, te entrega una poción extra y susurra: "
        "\"Los cultistas conocen el bosque. Ten cuidado con las emboscadas.\"\n\n"
        "Un bardo llamado Say, que estaba de paso en la taberna de Facundo, "
        "te detiene en la puerta y dice: \"He cantado sobre héroes toda mi vida. "
        "Si vuelves vivo, cantaré sobre ti.\"\n\n"
        "El camino al norte te espera.",
        titulo="Preparativos",
    )

    # Recompensa por aceptar la misión
    nueva_pocion = Item("Poción de Salud", "pocion", "Restaura 25 HP", 15, {"curacion": 25})
    personaje.inventario.append(nueva_pocion)
    ui.console.print("  [green]+1 Poción de Salud recibida[/green]")
    ui.pausa(0.8)
    ui.pedir_continuar()
    return "1_bosque"


@escena("1_bosque")
def escena_1_bosque(personaje, estado):
    ui.limpiar()
    ui.separador("green", "El Bosque Umbrío")
    ui.panel_narrativa(
        "El Bosque Umbrío se cierra sobre el camino como una boca que engulle la luz. "
        "Los árboles son tan altos y densos que apenas ves el cielo. "
        "El viento lleva voces, o quizás solo sea la imaginación.\n\n"
        "Pasas junto a un viejo letrero de madera tallado: \"Crosty el Explorador pasó por aquí. "
        "Si lees esto, date la vuelta.\" El consejo, por desgracia, llega tarde.\n\n"
        "A mitad del camino, algo no encaja. Las ramas están rotas hacia adentro. "
        "Las huellas en el barro son demasiado frescas. Alguien os está siguiendo.",
    )

    eleccion = ui.elegir_opcion([
        "Detenerte en silencio y escuchar atentamente.",
        "Continuar a paso rápido, ignorando las señales.",
        "Fingir que no has notado nada y prepararte para emboscar al emboscador.",
    ])

    if eleccion == 0:
        check = chequeo_habilidad(personaje.sabiduria, 13)
        ui.mostrar_resultado_chequeo(check, "Sabiduría", 13)
        if check["exito"]:
            ui.panel_narrativa(
                "Te detienes. Aguantas la respiración. "
                "Entre los matorrales escuchas el crujido de cuero y metal. "
                "Hay al menos tres. Sueltas tu arma de la vaina en silencio.\n\n"
                "Cuando se lanzan desde los árboles, ya estás listo. "
                "El primer cultista aterriza frente a una hoja que ya lo espera.",
                titulo="¡Detectado!",
                color="green",
            )
            estado["ventaja_combate"] = True
        else:
            ui.panel_narrativa(
                "Oyes el viento. Solo el viento. "
                "Un grito y tres cultistas saltan desde los árboles. La sorpresa es total.",
                titulo="Emboscada",
                color="red",
            )
            personaje.recibir_danio(8)

    elif eleccion == 1:
        ui.panel_narrativa(
            "Aceleras el paso. No es suficiente. "
            "Un silbido agudo y tres cultistas te cortan el camino desde la oscuridad.\n\n"
            "\"¡El intruso de Rocabruna!\" grita su líder. \"Malachar os temía. Qué decepción.\"",
            titulo="Emboscada",
            color="red",
        )
        personaje.recibir_danio(6)

    else:
        check = chequeo_habilidad(personaje.destreza, 14)
        ui.mostrar_resultado_chequeo(check, "Destreza", 14)
        if check["exito"]:
            ui.panel_narrativa(
                "Finges tranquilidad. Cuando el primero salta, ya tienes el arma en mano. "
                "Tu contraataque lo derriba antes de que toque el suelo.\n\n"
                "\"¡Imposible!\" grita otro. La batalla comienza con ventaja tuya.",
                titulo="¡Contraemboscada!",
                color="green",
            )
            estado["ventaja_combate"] = True
            personaje.decisiones_heroicas += 1
        else:
            ui.panel_narrativa(
                "La actuación no convence. Los cultistas atacan en masa. "
                "El plan era bueno, la ejecución... mejorable.",
                color="yellow",
            )
            personaje.recibir_danio(5)

    ui.pedir_continuar()
    return "1_combate_cultistas"


@escena("1_combate_cultistas")
def escena_1_combate_cultistas(personaje, estado):
    ui.limpiar()
    ui.panel_narrativa(
        "¡El Culto del Umbral te ataca! Su líder blandea un símbolo negro mientras "
        "sus seguidores te rodean con cuchillos de obsidiana.",
        titulo="¡COMBATE!",
        color="red",
    )

    if estado.get("ventaja_combate"):
        ui.console.print("[green]  Tienes ventaja: el primer golpe es tuyo.[/green]\n")
        personaje.decisiones_heroicas += 1

    enemigo = crear_enemigo("cultista")
    resultado = combate.iniciar_combate(personaje, enemigo)

    if not resultado["victoria"] and not resultado["huyo"]:
        return "game_over"

    if resultado["huyo"]:
        ui.panel_narrativa(
            "Escapas al bosque con el corazón latiendo desbocado. "
            "Rodeas el campamento por un camino más largo y llegas a las ruinas sin más incidentes.",
            titulo="Huida",
            color="yellow",
        )

    estado.pop("ventaja_combate", None)
    ui.pedir_continuar()
    return "1_ruinas_puertas"


@escena("1_ruinas_puertas")
def escena_1_ruinas_puertas(personaje, estado):
    ui.limpiar()
    ui.separador("dim white", "Las Puertas de las Ruinas de Yar")
    ui.panel_narrativa(
        "Las Ruinas de Yar emergen de la niebla como una cicatriz en el mundo. "
        "Columnas de piedra negra rodean una entrada oscura. "
        "En el dintel, inscripciones en un idioma antiguo brillan con luz violeta.\n\n"
        "Al pie de una columna, encuentras los restos de un campamento. "
        "Un diario a medio pudrir lleva el nombre del erudito Emilio de Velmoor. "
        "La última anotación dice: \"Las runas hablan de Zuñi el Sabio, "
        "primer guardián de Yar. Si su espíritu aún habita aquí, que nos proteja.\"\n\n"
        "Hay algo opresivo aquí. El aire huele a muerte vieja y a algo que no debería existir.",
    )

    eleccion = ui.elegir_opcion([
        "Estudiar las inscripciones del dintel.",
        "Inspeccionar el perímetro antes de entrar.",
        "Entrar directamente, sin perder tiempo.",
    ])

    if eleccion == 0:
        check = chequeo_habilidad(personaje.inteligencia, 14)
        ui.mostrar_resultado_chequeo(check, "Inteligencia", 14)
        if check["exito"]:
            ui.panel_narrativa(
                "Reconoces fragmentos de Aryndico antiguo. "
                "\"...quien cruce sin luz en el corazón, despertará a los guardianes...\"\n\n"
                "Una advertencia. Pero también algo más: un símbolo de protección "
                "que grabas en tu palma con carbón. Sabrás usarlo.",
                titulo="Conocimiento Arcano",
                color="blue",
            )
            personaje.flags["conoce_runas"] = True
            personaje.agregar_xp(30)
        else:
            ui.panel_narrativa(
                "El lenguaje es demasiado antiguo. Solo reconoces una palabra: \"muerte\".",
                color="yellow",
            )

    elif eleccion == 1:
        check = chequeo_habilidad(personaje.destreza, 12)
        ui.mostrar_resultado_chequeo(check, "Destreza", 12)
        if check["exito"]:
            ui.panel_narrativa(
                "Encuentras las huellas frescas de varios cultistas. "
                "Calculando... llegaron hace menos de dos horas. "
                "También encuentras una poción olvidada junto a una hoguera apagada.",
                titulo="Exploración",
                color="green",
            )
            personaje.inventario.append(Item("Poción Arcana", "pocion", "Restaura 20 MP", 20, {"mp": 20}))
            personaje.agregar_xp(20)
        else:
            ui.panel_narrativa("No encuentras nada relevante en el perímetro.", color="dim white")

    else:
        ui.panel_narrativa(
            "Entras con paso firme. Si hay peligro, lo afrontarás de frente.",
            titulo="Valentía",
            color="yellow",
        )
        personaje.decisiones_heroicas += 1

    ui.pedir_continuar()

    ui.panel_narrativa(
        "Das el primer paso dentro de las Ruinas de Yar. "
        "La oscuridad se cierra a tu alrededor. Fin del Arco I.",
        titulo="Fin del Arco I",
        color="gold1",
    )
    ui.pedir_continuar()
    return "2_intro"


# ==============================================================================
#  ARCO 2: LAS RUINAS DE YAR
# ==============================================================================

@escena("2_intro")
def escena_2_intro(personaje, estado):
    ui.limpiar()
    ui.separador("cyan", "ARCO II — Las Ruinas de Yar")
    ui.panel_narrativa(
        "Las Ruinas de Yar son un laberinto de piedra negra y silencio. "
        "Antorchas antiguas se encienden solas a tu paso, como si el lugar te reconociera. "
        "O te estuviera estudiando.\n\n"
        "Desciendes por escaleras que parecen no tener fin, hasta llegar a una bifurcación. "
        "La galería izquierda huele a polvo y huesos. La derecha, a algo más reciente: "
        "sangre y magia oscura.",
    )

    eleccion = ui.elegir_opcion([
        "Tomar la galería izquierda, más antigua y silenciosa.",
        "Tomar la galería derecha, donde está la actividad reciente.",
        "Buscar un tercer camino oculto en la pared.",
    ])

    if eleccion == 0:
        estado["camino_elegido"] = "izquierda"
        ui.panel_narrativa(
            "La galería izquierda está repleta de murales milenarios. "
            "Representan la historia de Yar: el sabio Zuñi y su orden de guardianes "
            "que sellaron a un dios caótico usando el mismo artefacto que ahora busca Malachar.\n\n"
            "Un mural muestra a una bestia legendaria llamada Bolo, "
            "un coloso de roca que protegía la entrada del templo. "
            "Por su expresión tallada, no parecía amigable.\n\n"
            "El camino es más seguro, pero más largo.",
            titulo="La Galería de los Ancestros",
        )
        personaje.agregar_xp(25)
        personaje.flags["conoce_historia_yar"] = True

    elif eleccion == 1:
        estado["camino_elegido"] = "derecha"
        ui.panel_narrativa(
            "La galería derecha lleva directamente al corazón de las ruinas. "
            "También hay trampas recién activadas y símbolos del Culto del Umbral en las paredes. "
            "Malachar ya ha pasado por aquí.",
            titulo="El Camino del Culto",
            color="red",
        )

    else:
        check = chequeo_habilidad(personaje.inteligencia, 15)
        ui.mostrar_resultado_chequeo(check, "Inteligencia", 15)
        if check["exito"]:
            estado["camino_elegido"] = "secreto"
            ui.panel_narrativa(
                "Presionas una piedra que sobresale apenas un centímetro de la pared. "
                "Con un crujido milenario, se abre un pasaje secreto.\n\n"
                "Este camino conduce directamente a la cámara central, "
                "evitando las trampas principales. Y hay un cofre abandonado en el camino.",
                titulo="Pasaje Secreto",
                color="cyan",
            )
            personaje.inventario.append(
                Item("Amuleto de Protección", "magico",
                     "Aumenta armadura en +2 durante el día", 80, {"armadura": 2})
            )
            personaje.armadura += 2
            personaje.agregar_xp(40)
        else:
            estado["camino_elegido"] = "izquierda"
            ui.panel_narrativa(
                "No encuentras ningún pasaje oculto. Optas por la galería izquierda.",
                color="dim white",
            )

    ui.pedir_continuar()
    return "2_trampa"


@escena("2_trampa")
def escena_2_trampa(personaje, estado):
    ui.limpiar()
    camino = estado.get("camino_elegido", "izquierda")

    if camino == "secreto":
        ui.panel_narrativa(
            "El pasaje secreto te lleva directamente a la Cámara del Eco "
            "sin ningún obstáculo. La suerte está de tu lado.",
            titulo="Paso Libre",
            color="green",
        )
        ui.pedir_continuar()
        return "2_camara_eco"

    ui.panel_narrativa(
        "Avanzas por la galería cuando el suelo cruje bajo tus pies de forma extraña. "
        "Un segundo demasiado tarde lo reconoces: placa de presión.",
    )

    check = chequeo_habilidad(personaje.destreza, 14)
    ui.mostrar_resultado_chequeo(check, "Destreza", 14)

    if check["exito"]:
        ui.panel_narrativa(
            "Tu instinto te salva. Te lanzas hacia un lado justo cuando una "
            "ráfaga de dardos envenedados silba por donde estabas parado.\n\n"
            "Examinas la trampa. Hay más adelante. Ya sabes cómo evitarlas.",
            titulo="Esquivado",
            color="green",
        )
    else:
        danio = tirar_dado(6) + 2
        personaje.recibir_danio(danio)
        ui.panel_narrativa(
            f"Los dardos te alcanzan en el costado. "
            f"El veneno es suave —gracias a los dioses— pero el dolor es real.\n\n"
            f"Pierdes {danio} HP. Necesitarás cuidarte.",
            titulo="Impactado",
            color="red",
        )
        ui.console.print(f"  [red]-{danio} HP (HP actual: {personaje.hp_actual}/{personaje.hp_max})[/red]")

    ui.pedir_continuar()
    return "2_camara_eco"


@escena("2_camara_eco")
def escena_2_camara_eco(personaje, estado):
    ui.limpiar()
    ui.separador("cyan", "La Cámara del Eco")
    ui.panel_narrativa(
        "Llegas a una vasta cámara circular. En el centro, un altar de obsidiana. "
        "Sobre él, una esfera de cristal negro que pulsa con luz violeta.\n\n"
        "Pero antes de poder acercarte, tres esqueletos guerreros se levantan de sus nichos "
        "en las paredes. Sus cuencas vacías brillan con el mismo color violeta.\n\n"
        "Uno es más grande que los otros. Sus huesos están reforzados con metal negro.",
        titulo="¡Guardianes Despertados!",
        color="red",
    )

    eleccion = ui.elegir_opcion([
        "Luchar contra los tres a la vez.",
        "Buscar una forma de dividirlos para enfrentarlos uno a uno.",
        "Usar el conocimiento de las runas (si lo tienes) para intentar detenerlos.",
    ])

    if eleccion == 2 and personaje.flags.get("conoce_runas"):
        check = chequeo_habilidad(personaje.inteligencia, 15)
        ui.mostrar_resultado_chequeo(check, "Inteligencia", 15)
        if check["exito"]:
            ui.panel_narrativa(
                "Trazas el símbolo de protección en el aire. Una luz dorada emana de tu mano.\n\n"
                "Los dos esqueletos menores se detienen. Sus huesos se separan y caen "
                "en montones inertes. Solo el guardián mayor permanece en pie, "
                "pero parece debilitado.",
                titulo="Las Runas Funcionan",
                color="gold1",
            )
            enemigo = crear_enemigo("esqueleto")
            enemigo.hp_actual = enemigo.hp_max // 2
            enemigo.nombre = "Guardián Marchito"
            personaje.agregar_xp(60)
        else:
            ui.panel_narrativa(
                "Las runas no responden como esperabas. Los guardianes avanzan.",
                color="red",
            )
            enemigo = crear_enemigo("esqueleto")
            personaje.recibir_danio(8)
    elif eleccion == 1:
        check = chequeo_habilidad(personaje.destreza, 13)
        ui.mostrar_resultado_chequeo(check, "Destreza", 13)
        if check["exito"]:
            ui.panel_narrativa(
                "Derribas una columna entre los guardianes, bloqueando el paso de dos de ellos. "
                "Solo uno llega a ti. La estrategia funciona.",
                titulo="Dividir y Vencer",
                color="green",
            )
            enemigo = crear_enemigo("esqueleto")
            personaje.agregar_xp(20)
        else:
            ui.panel_narrativa(
                "Los tres te rodean. No hay salida fácil.",
                color="red",
            )
            enemigo = crear_enemigo("esqueleto")
            personaje.recibir_danio(10)
    else:
        ui.panel_narrativa(
            "Los tres guardianes se lanzan sobre ti. Es una batalla caótica y brutal.",
            color="red",
        )
        enemigo = crear_enemigo("esqueleto")
        personaje.recibir_danio(12)

    resultado = combate.iniciar_combate(personaje, enemigo)
    if not resultado["victoria"] and not resultado["huyo"]:
        return "game_over"

    ui.pedir_continuar()
    return "2_artefacto"


@escena("2_artefacto")
def escena_2_artefacto(personaje, estado):
    ui.limpiar()
    ui.separador("bright_magenta", "El Artefacto de Yar")
    ui.panel_narrativa(
        "Con los guardianes caídos, te acercas al altar.\n\n"
        "La esfera de cristal negro late como un corazón. "
        "Al tocarla, imágenes te invaden la mente: "
        "un lich de huesos blancos y ojos de fuego violeta. "
        "Una torre negra en una llanura muerta. Un portal enorme que se abre hacia la oscuridad.\n\n"
        "Escuchas una voz que viene de todas partes:\n\n"
        "\"Llegas tarde, héroe. El Artefacto ya no está aquí. "
        "Solo dejé este recuerdo para que vieras lo que viene. "
        "Encuéntrame en mi torre. Si te atreves.\"",
        titulo="Malachar",
        color="bright_magenta",
    )

    ui.pedir_continuar()
    ui.panel_narrativa(
        "La esfera se apaga. En el altar encuentras grabado un mapa: "
        "La Torre de Malachar se alza en las Llanuras de Ceniza, al este de las ruinas.\n\n"
        "También encuentras lo que Malachar dejó atrás: una daga imbuida de energía arcana. "
        "Una provocación. O un regalo. No estás seguro de cuál.",
        titulo="Lo que queda",
    )

    personaje.inventario.append(
        Item("Daga del Umbral", "arma", "Arma imbuida de magia oscura. +2 al daño.", 120, {"bonus_danio": 2})
    )
    personaje.dado_danio = min(12, personaje.dado_danio + 1)
    personaje.agregar_xp(80)
    ui.console.print("[cyan]  + Daga del Umbral recibida (dado de daño mejorado)[/cyan]")
    ui.console.print("[magenta]  + 80 XP[/magenta]")
    ui.pausa(0.8)
    ui.pedir_continuar()

    ui.panel_narrativa(
        "Sales de las Ruinas de Yar con más preguntas que respuestas. "
        "Pero el camino está claro: la Torre de Malachar.\n\n"
        "Fin del Arco II.",
        titulo="Fin del Arco II",
        color="gold1",
    )
    ui.pedir_continuar()
    return "3_intro"


# ==============================================================================
#  ARCO 3: LA TORRE DE MALACHAR
# ==============================================================================

@escena("3_intro")
def escena_3_intro(personaje, estado):
    ui.limpiar()
    ui.separador("bright_magenta", "ARCO III — La Torre de Malachar")
    ui.panel_narrativa(
        "Las Llanuras de Ceniza viven a su nombre. "
        "La tierra aquí es gris y estéril. No hay pájaros, no hay viento, no hay vida. "
        "Solo la Torre de Malachar, un monolito negro que perfora las nubes al horizonte.\n\n"
        "El camino lleva varios días. Y en el camino, encuentras algo inesperado.",
    )
    ui.pedir_continuar()

    ui.panel_narrativa(
        "Una pequeña aldea. O lo que queda de ella.\n\n"
        "Los habitantes de Amberfall sobreviven en medio de la desolación. "
        "Son apenas cincuenta personas: ancianos, niños, heridos. "
        "Un viejo mercader llamado Pedrilio reparte sus últimas raciones entre los niños.\n\n"
        "Su líder, una mujer llamada Lyris, te sale al encuentro con los ojos enrojecidos:\n\n"
        "\"Los cultistas nos saquearon hace tres días. Se llevaron todo. "
        "No tenemos comida para la próxima semana. "
        "Pero escucha... sé dónde hay suministros del Culto. "
        "Si me ayudas a recuperarlos, te puedo dar información valiosa sobre la Torre.\"",
        titulo="Amberfall",
    )

    eleccion = ui.elegir_opcion([
        "Aceptar ayudar a Lyris y recuperar los suministros.",
        "No tienes tiempo, la Torre es la prioridad.",
        "Dejarles tus pociones y oro como ayuda, pero seguir tu camino.",
    ])

    if eleccion == 0:
        personaje.decisiones_heroicas += 1
        personaje.flags["ayudo_amberfall"] = True
        ui.panel_narrativa(
            "El campamento de los cultistas está a media hora de la aldea. "
            "Con un ataque rápido y sorpresivo, recuperas las provisiones.\n\n"
            "Lyris te abraza con lágrimas en los ojos. "
            "Y cumple su palabra: te da un pergamino con el mapa interior de la Torre "
            "y una debilidad crucial de Malachar: el lich necesita su filacteria "
            "—un amuleto negro que lleva al cuello— para regenerarse. "
            "Si lo destruyes durante el combate, no podrá recuperarse.",
            titulo="Los Héroes también Ayudan",
            color="green",
        )
        personaje.agregar_xp(100)
        personaje.flags["conoce_filacteria"] = True
        personaje.inventario.append(
            Item("Pergamino del Caos", "magico", "Mapa interior de la Torre de Malachar", 0)
        )

    elif eleccion == 1:
        ui.panel_narrativa(
            "\"Entiendo\", dice Lyris con voz fría. \"Que los dioses te acompañen, entonces.\"\n\n"
            "Sigues tu camino con la vista al frente. "
            "En la Torre no habrá nadie que te dé información. "
            "Tendrás que descubrirlo todo por tu cuenta.",
            titulo="La Misión ante Todo",
            color="yellow",
        )

    else:
        personaje.decisiones_heroicas += 1
        personaje.flags["ayudo_amberfall"] = True
        pociones_dadas = sum(1 for i in personaje.inventario if i.tipo == "pocion")
        personaje.inventario = [i for i in personaje.inventario if i.tipo != "pocion"]
        oro_dado = min(personaje.oro, 30)
        personaje.oro -= oro_dado
        ui.panel_narrativa(
            f"Les dejas tus pociones y {oro_dado} monedas de oro. "
            f"No es suficiente para recuperar lo perdido, pero ayudará.\n\n"
            "Lyris asiente con gratitud. \"Que tu camino sea recto, héroe.\"",
            titulo="Un Gesto de Bondad",
            color="green",
        )
        personaje.agregar_xp(60)

    ui.pedir_continuar()
    return "3_torre_entrada"


@escena("3_torre_entrada")
def escena_3_torre_entrada(personaje, estado):
    ui.limpiar()
    ui.separador("dark_red", "La Torre de Malachar")
    ui.panel_narrativa(
        "La Torre de Malachar es más imponente de cerca. "
        "Cien metros de piedra negra, sin ventanas, sin ornamentos. "
        "Solo un portal de hierro en la base, grabado con el mismo símbolo que viste en las ruinas.\n\n"
        "Justo cuando vas a entrar, el portal se abre solo. Desde adentro viene una voz amplificada por magia:\n\n"
        "\"Bienvenido, héroe de Rocabruna. He estado esperando. "
        "Mi guardián está ansioso por conocerte. "
        "Espero que hayas disfrutado el viaje, porque termina aquí.\"",
        titulo="La Voz de Malachar",
        color="bright_magenta",
    )

    ui.pedir_continuar()
    ui.panel_narrativa(
        "El interior de la torre es una sala circular enorme. "
        "En el centro, una figura colosal: un gólem de obsidiana volcánica. "
        "Sus ojos son cristales rojos que emiten calor. "
        "Cuando te ve, un sonido como un trueno retumba en la sala.",
        titulo="El Guardián",
        color="red",
    )

    eleccion = ui.elegir_opcion([
        "Atacar al gólem directamente.",
        "Buscar sus puntos débiles antes de atacar.",
        "Intentar escalar a las escaleras detrás del gólem.",
    ])

    if eleccion == 1:
        check = chequeo_habilidad(personaje.inteligencia, 14)
        ui.mostrar_resultado_chequeo(check, "Inteligencia", 14)
        if check["exito"]:
            ui.panel_narrativa(
                "Observas el gólem. Las costuras entre las piedras de obsidiana "
                "vibran cuando se mueve. Los cristales rojos de sus ojos son la fuente de su energía.\n\n"
                "Si rompes uno de sus cristales oculares, su defensa bajará considerablemente.",
                titulo="Análisis Táctico",
                color="green",
            )
            estado["tactica_golem"] = True
            personaje.agregar_xp(30)
        else:
            ui.panel_narrativa("No encuentras ninguna debilidad evidente. La lucha será dura.", color="yellow")

    elif eleccion == 2:
        check = chequeo_habilidad(personaje.destreza, 16)
        ui.mostrar_resultado_chequeo(check, "Destreza", 16)
        if check["exito"]:
            ui.panel_narrativa(
                "Intentas rodear al gólem. Casi lo logras.\n\n"
                "Casi. Una mano del tamaño de un caballo te aplasta contra la pared. "
                "El gólem no puede ser evadido. Tendrás que luchar.",
                color="yellow",
            )
            personaje.recibir_danio(15)
        else:
            personaje.recibir_danio(20)
            ui.panel_narrativa(
                "El gólem te alcanza. El impacto es brutal. "
                "Tu cuerpo vuela varios metros. Cuando te levantas, te duele absolutamente todo.",
                color="red",
            )

    ui.pedir_continuar()
    return "3_combate_golem"


@escena("3_combate_golem")
def escena_3_combate_golem(personaje, estado):
    ui.limpiar()
    ui.panel_narrativa(
        "¡El Gólem de Obsidiana levanta sus puños y ataca! "
        "El suelo tiembla con cada uno de sus pasos.",
        titulo="¡BOSS: Gólem de Obsidiana!",
        color="red",
    )

    enemigo = crear_enemigo("golem_obsidiana")

    if estado.get("tactica_golem"):
        enemigo.armadura -= 3
        ui.console.print("[green]  Tu análisis táctico reduce su armadura efectiva.[/green]\n")

    resultado = combate.iniciar_combate(personaje, enemigo)
    if not resultado["victoria"] and not resultado["huyo"]:
        return "game_over"

    estado.pop("tactica_golem", None)
    ui.pedir_continuar()
    return "3_escalada"


@escena("3_escalada")
def escena_3_escalada(personaje, estado):
    ui.limpiar()
    ui.panel_narrativa(
        "Con el gólem destruido, subes las escaleras en espiral de la torre. "
        "Cada piso está lleno de escrituras en las paredes: planes de Malachar. "
        "El ritual para abrir el portal se completa esta noche, con la luna oscura.\n\n"
        "No tienes mucho tiempo.",
    )

    ui.panel_narrativa(
        "En el penúltimo piso encuentras algo que no esperabas: "
        "a un hombre llamado Payardo, uno de los cultistas de Rocabruna, encadenado a la pared.\n\n"
        "\"Por favor... Malachar me engañó. Prometió poder y gloria. "
        "Solo quería... quería ser alguien. Ahora mira dónde terminé.\"\n\n"
        "Payardo llora. Está desarmado e indefenso.",
    )

    eleccion = ui.elegir_opcion([
        "Liberarlo y decirle que huya.",
        "Dejarlo ahí, no hay tiempo para más.",
        "Preguntarle sobre Malachar antes de decidir.",
    ])

    if eleccion == 0:
        personaje.decisiones_heroicas += 1
        ui.panel_narrativa(
            "Rompes las cadenas de Payardo. Solloza de alivio.\n\n"
            "\"Gracias. Gracias, héroe. El lich... su filacteria es un cráneo de cristal negro. "
            "Lo lleva colgado al cuello. Si la destruyes durante la pelea, no podrá regenerarse.\"\n\n"
            "Payardo huye escaleras abajo. Tienes información valiosa.",
            titulo="Misericordia",
            color="green",
        )
        personaje.flags["conoce_filacteria"] = True
        personaje.agregar_xp(50)

    elif eleccion == 2:
        check = chequeo_habilidad(personaje.carisma, 12)
        ui.mostrar_resultado_chequeo(check, "Carisma", 12)
        if check["exito"]:
            ui.panel_narrativa(
                "El cultista, agradecido por tu interés, te revela todo lo que sabe: "
                "la ubicación de la filacteria, el patrón de ataque del lich y "
                "que sus hechizos son más débiles si has destruido partes del ritual.",
                titulo="Información Obtenida",
                color="cyan",
            )
            personaje.flags["conoce_filacteria"] = True
            personaje.flags["conoce_patron"] = True
            personaje.agregar_xp(40)
        else:
            ui.panel_narrativa("El cultista está demasiado aterrorizado para hablar con coherencia.", color="yellow")

    else:
        ui.panel_narrativa(
            "\"No tengo tiempo para ti.\"\n\n"
            "Sus gritos de súplica te acompañan mientras subes las escaleras.",
            color="dim",
        )

    ui.pedir_continuar()
    return "3_camara_final"


@escena("3_camara_final")
def escena_3_camara_final(personaje, estado):
    ui.limpiar()
    ui.separador("bright_magenta", "La Cámara del Lich")
    ui.panel_narrativa(
        "La cima de la torre es una cámara abierta al cielo. "
        "La luna está completamente oscura. Las estrellas... las estrellas se están apagando. "
        "Una a una, como si alguien las borrara del cielo.\n\n"
        "En el centro de la cámara, sobre un círculo de runas ardientes, está Malachar.\n\n"
        "Es más aterrador que cualquier visión. Un esqueleto alto y delgado envuelto en "
        "túnicas negras que flotan como si estuviera bajo el agua. "
        "Dos llamas violetas arden donde deberían estar sus ojos. "
        "En su cuello, un pequeño cráneo de cristal negro late como un corazón.",
    )
    ui.pausa(1.5)
    ui.panel_narrativa(
        "\"Llegas justo a tiempo para ver el fin del mundo.\"\n\n"
        "Su voz es como el polvo de tumbas olvidadas.\n\n"
        "\"Llevo siglos preparando esto. Viví, morí, renacé y morí de nuevo, "
        "solo para llegar a esta noche. ¿Crees que una sola persona puede detener "
        "lo inevitable?\"\n\n"
        "Detrás de él, el portal oscuro empieza a abrirse. "
        "Formas sin nombre se asoman desde el otro lado.",
        titulo="Malachar habla",
        color="bright_magenta",
    )

    eleccion = ui.elegir_opcion([
        "\"Sí. Eso es exactamente lo que creo.\" — Atacar sin más palabras.",
        "Intentar dialogar para ganar tiempo y buscar una abertura.",
        "Lanzarte hacia el portal para intentar cerrarlo antes del combate.",
    ])

    if eleccion == 0:
        personaje.decisiones_heroicas += 1
        ui.panel_accion("¡Te lanzas hacia Malachar con todo!", color="red")
        if personaje.flags.get("conoce_filacteria"):
            ui.console.print("[green]  Sabes del cráneo de cristal. Irás directo a por él.[/green]")

    elif eleccion == 1:
        check = chequeo_habilidad(personaje.carisma, 13)
        ui.mostrar_resultado_chequeo(check, "Carisma", 13)
        if check["exito"]:
            ui.panel_narrativa(
                "\"Interesante\", dice Malachar. \"Un humano que prefiere hablar a morir.\"\n\n"
                "Mientras hablas, observas sus patrones. El lich se mueve en círculos "
                "cuando conjura. Un lado es su punto ciego. Lo usarás.",
                titulo="Táctico",
                color="cyan",
            )
            estado["ventaja_malachar"] = True
            personaje.agregar_xp(30)
        else:
            ui.panel_narrativa(
                "\"Las palabras no tienen poder aquí\", responde el lich. "
                "\"Solo la muerte.\" Y lanza el primer hechizo.",
                color="red",
            )
            personaje.recibir_danio(18)

    else:
        check = chequeo_habilidad(personaje.destreza, 17)
        ui.mostrar_resultado_chequeo(check, "Destreza", 17)
        if check["exito"]:
            ui.panel_narrativa(
                "¡Llegas al portal! Tus manos tocan el borde ardiente.\n\n"
                "Con un esfuerzo sobrehumano comienzas a cerrarlo. Las formas del otro lado "
                "aúllan de rabia. El portal se estrecha.\n\n"
                "Malachar ruge y te golpea, lanzándote de vuelta. "
                "Pero el daño está hecho: el portal está debilitado. "
                "El ritual ha fallado a medias. Malachar está furioso.",
                titulo="Acto Heroico",
                color="gold1",
            )
            personaje.recibir_danio(20)
            estado["portal_dañado"] = True
            personaje.decisiones_heroicas += 1
            personaje.agregar_xp(80)
        else:
            ui.panel_narrativa(
                "Malachar te lo impide. Una barrera mágica te rechaza con violencia.",
                color="red",
            )
            personaje.recibir_danio(25)

    if personaje.hp_actual <= 0:
        return "game_over"

    ui.pedir_continuar()
    return "3_combate_malachar"


@escena("3_combate_malachar")
def escena_3_combate_malachar(personaje, estado):
    ui.limpiar()
    ui.panel_narrativa(
        "¡El momento que definirá el destino de Eryndor ha llegado!\n\n"
        "Malachar extiende sus manos esqueléticas. Energía oscura chisporrotea entre sus dedos. "
        "Las runas en el suelo arden. Las estrellas siguen apagándose.\n\n"
        "Esta es la batalla final.",
        titulo="¡JEFE FINAL: MALACHAR EL LICH ETERNO!",
        color="bright_magenta",
    )

    enemigo = crear_enemigo("malachar")

    if estado.get("ventaja_malachar"):
        enemigo.armadura -= 2
        ui.console.print("[green]  Tu análisis reduce su armadura efectiva.[/green]\n")
    if estado.get("portal_dañado"):
        enemigo.habilidad_chance -= 0.15
        enemigo.regenera = max(0, enemigo.regenera - 4)
        ui.console.print("[green]  El ritual dañado debilita sus poderes de regeneración.[/green]\n")
    if personaje.flags.get("conoce_filacteria"):
        ui.console.print("[cyan]  Sabes de la filacteria. Tienes ventaja adicional.[/cyan]\n")
        enemigo.hp_max = int(enemigo.hp_max * 0.85)
        enemigo.hp_actual = enemigo.hp_max

    resultado = combate.iniciar_combate(personaje, enemigo)
    if not resultado["victoria"] and not resultado["huyo"]:
        return "game_over"

    estado.pop("ventaja_malachar", None)
    estado.pop("portal_dañado", None)
    ui.pedir_continuar()
    return "3_epilogo"


@escena("3_epilogo")
def escena_3_epilogo(personaje, estado):
    ui.limpiar()
    ui.separador("gold1", "Epílogo")
    ui.panel_narrativa(
        "Malachar cae. La filacteria explota en mil pedazos de cristal negro que se deshacen "
        "en humo antes de tocar el suelo.\n\n"
        "El portal colapsa con un sonido como el fin del mundo. Las formas que se asomaban "
        "desde el otro lado dan un último aullido y desaparecen.\n\n"
        "Uno a uno, como si alguien los encendiera de nuevo, los estrellas vuelven al cielo.\n\n"
        "Silencio.",
        titulo="El Fin de Malachar",
        color="gold1",
    )
    ui.pedir_continuar()

    # Epilogo personalizado según decisiones
    ui.panel_narrativa(
        f"Los días que siguen son extrañamente tranquilos.\n\n"
        f"Las noticias se extienden rápido: el Culto del Umbral se desintegra "
        f"sin su líder. Los cultistas abandonan sus túnicas y vuelven a sus aldeas, "
        f"avergonzados pero vivos.\n\n"
        f"Rocabruna reconstruye. Facundo reabre la taberna y el hidromiel fluye como nunca. "
        f"Peter es nombrado capitán de la guardia. Martha sigue curando a los enfermos con su sonrisa inquebrantable.\n\n"
        f"Pedrilio, el mercader de Amberfall, abre una ruta de comercio entre las aldeas liberadas. "
        f"La prosperidad vuelve lentamente a las tierras.",
        titulo="El Mundo Después",
    )

    if personaje.flags.get("salvo_nino"):
        ui.panel_narrativa(
            f"El niño que salvaste de la herrería, Aldric, crece para convertirse "
            f"en el mejor herrero de la región. Cada espada que forja lleva grabado "
            f"un símbolo: tu nombre. Facundo le enseña a servir hidromiel cuando no está martillando.",
        )
    if personaje.flags.get("ayudo_amberfall"):
        ui.panel_narrativa(
            "Lyris de Amberfall escribe una crónica de tus hazañas. "
            "La lee en cada aldea que visita. Tu nombre llega a todos los rincones de Eryndor.\n\n"
            "Payardo, el cultista arrepentido que liberaste en la torre, "
            "se convierte en su escolta. \"Le debo la vida\", dice cuando le preguntan por qué.",
        )

    if personaje.decisiones_heroicas >= 3:
        ui.panel_narrativa(
            f"El bardo Say compone una canción épica sobre {personaje.nombre}, el {personaje.clase} "
            f"que salvó el mundo no una, sino varias veces en un solo viaje. "
            f"Crosty el Explorador la lleva a tierras lejanas. "
            f"Emilio la transcribe en los archivos de la Gran Biblioteca.\n\n"
            f"Zuñi, el espíritu guardián de Yar, finalmente descansa en paz. "
            f"Cuentan que su fantasma sonríe por primera vez en mil años.\n\n"
            f"La leyenda crece. La gente añade detalles. "
            f"Ya no importa cuáles son reales: todos lo son.",
            titulo="Una Leyenda Nace",
            color="gold1",
        )
    else:
        ui.panel_narrativa(
            f"Say el bardo canta sobre ti en tabernas vacías. "
            f"Nadie más conoce tu nombre. Y quizás así lo prefieres. "
            f"El mundo sigue girando, vivo, gracias a lo que hiciste esta noche.",
            titulo="El Héroe Silencioso",
        )

    ui.panel_narrativa(
        f"Estadísticas finales de {personaje.nombre}:\n\n"
        f"  Nivel alcanzado: {personaje.nivel}\n"
        f"  Enemigos derrotados: {personaje.enemigos_derrotados}\n"
        f"  Decisiones heroicas: {personaje.decisiones_heroicas}\n"
        f"  Oro acumulado: {personaje.oro} monedas\n"
        f"  Rasgos de personalidad: {', '.join(personaje.rasgos) if personaje.rasgos else 'desconocidos'}",
        titulo="Fin de la Aventura",
        color="gold1",
    )

    ui.pedir_continuar("Presiona Enter para volver al menú principal...")
    return "fin"


# ==============================================================================
#  GAME OVER
# ==============================================================================

@escena("game_over")
def escena_game_over(personaje, estado):
    ui.limpiar()
    ui.console.print()
    ui.separador("red", "Has Caído")
    ui.panel_narrativa(
        f"La oscuridad se cierra sobre {personaje.nombre}.\n\n"
        f"La batalla fue dura. Quizás demasiado. Pero incluso en la derrota, "
        f"tu valentía habrá sido recordada por quienes te conocieron.\n\n"
        f"Las leyendas no siempre terminan bien. A veces solo terminan.",
        titulo="Derrota",
        color="red",
    )
    ui.pedir_continuar("Presiona Enter para volver al menú...")
    return "fin"
