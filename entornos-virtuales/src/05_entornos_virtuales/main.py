# -*- coding: utf-8 -*-
def saludar(nombre: str) -> str:
    """Devuelve un saludo personalizado."""
    return f"Hola, {nombre}"


if __name__ == "__main__":
    print(saludar("Mundo"))
