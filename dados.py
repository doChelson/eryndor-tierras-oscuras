import random


def tirar_dado(caras: int) -> int:
    return random.randint(1, caras)


def tirar_dados(caras: int, cantidad: int) -> list:
    return [random.randint(1, caras) for _ in range(cantidad)]


def chequeo_habilidad(stat: int, dificultad: int) -> dict:
    """Chequeo estilo D&D: d20 + modificador vs dificultad."""
    modificador = (stat - 10) // 2
    dado = random.randint(1, 20)
    total = dado + modificador
    return {
        "dado": dado,
        "modificador": modificador,
        "total": total,
        "exito": total >= dificultad or dado == 20,
        "critico_exito": dado == 20,
        "critico_fallo": dado == 1,
    }


def tirada_ataque(bonus_ataque: int, armadura_enemigo: int) -> dict:
    dado = random.randint(1, 20)
    total = dado + bonus_ataque
    return {
        "dado": dado,
        "bonus": bonus_ataque,
        "total": total,
        "impacto": dado == 20 or total >= armadura_enemigo,
        "critico": dado == 20,
        "pifia": dado == 1,
    }


def tirada_danio(dado_caras: int, modificador: int = 0, critico: bool = False) -> dict:
    cantidad = 2 if critico else 1
    dados = tirar_dados(dado_caras, cantidad)
    total = max(1, sum(dados) + modificador)
    return {"dados": dados, "modificador": modificador, "total": total, "critico": critico}
