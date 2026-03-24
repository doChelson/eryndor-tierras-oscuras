import sys


def verificar_dependencias():
    try:
        import rich
    except ImportError:
        print("\n[ERROR] Falta la librería 'rich'.")
        print("Instálala con:  pip install rich\n")
        sys.exit(1)


def main():
    verificar_dependencias()
    import juego
    try:
        juego.iniciar()
    except KeyboardInterrupt:
        print("\n\n  Hasta pronto, aventurero.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
