import json
import os
from pathlib import Path

CARPETA_GUARDADO = Path.home() / ".dnd_eryndor"
ARCHIVO_GUARDADO = CARPETA_GUARDADO / "partida.json"


def guardar(personaje, estado: dict):
    CARPETA_GUARDADO.mkdir(exist_ok=True)
    from personaje import Item
    datos = {
        "personaje": {
            "nombre": personaje.nombre,
            "clase": personaje.clase,
            "nivel": personaje.nivel,
            "experiencia": personaje.experiencia,
            "fuerza": personaje.fuerza,
            "destreza": personaje.destreza,
            "inteligencia": personaje.inteligencia,
            "constitucion": personaje.constitucion,
            "sabiduria": personaje.sabiduria,
            "carisma": personaje.carisma,
            "hp_max": personaje.hp_max,
            "hp_actual": personaje.hp_actual,
            "mp_max": personaje.mp_max,
            "mp_actual": personaje.mp_actual,
            "dado_danio": personaje.dado_danio,
            "armadura": personaje.armadura,
            "oro": personaje.oro,
            "rasgos": personaje.rasgos,
            "habilidad_especial": personaje.habilidad_especial,
            "habilidad_usos": personaje.habilidad_usos,
            "habilidad_costo_mp": personaje.habilidad_costo_mp,
            "enemigos_derrotados": personaje.enemigos_derrotados,
            "decisiones_heroicas": personaje.decisiones_heroicas,
            "flags": personaje.flags,
            "inventario": [
                {
                    "nombre": i.nombre,
                    "tipo": i.tipo,
                    "descripcion": i.descripcion,
                    "valor_oro": i.valor_oro,
                    "efecto": i.efecto,
                }
                for i in personaje.inventario
            ],
        },
        "estado": estado,
    }
    with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def cargar():
    if not ARCHIVO_GUARDADO.exists():
        return None, None
    try:
        with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as f:
            datos = json.load(f)

        from personaje import Personaje, Item, crear_personaje
        pd = datos["personaje"]
        personaje = crear_personaje(pd["nombre"], pd["clase"], pd.get("rasgos", []))

        # Sobreescribir con datos guardados
        for campo in ["nivel", "experiencia", "fuerza", "destreza", "inteligencia",
                      "constitucion", "sabiduria", "carisma", "hp_max", "hp_actual",
                      "mp_max", "mp_actual", "dado_danio", "armadura", "oro",
                      "habilidad_usos", "enemigos_derrotados", "decisiones_heroicas"]:
            setattr(personaje, campo, pd[campo])

        personaje.flags = pd.get("flags", {})
        personaje.inventario = [
            Item(i["nombre"], i["tipo"], i["descripcion"], i["valor_oro"], i["efecto"])
            for i in pd.get("inventario", [])
        ]

        return personaje, datos["estado"]
    except Exception:
        return None, None


def existe_guardado() -> bool:
    return ARCHIVO_GUARDADO.exists()


def borrar_guardado():
    if ARCHIVO_GUARDADO.exists():
        ARCHIVO_GUARDADO.unlink()
