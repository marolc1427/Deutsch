#!/usr/bin/env python3
import os
import json


def list_json_files(dirpath):
    files = []
    for fname in sorted(os.listdir(dirpath)):
        if fname.endswith('.json'):
            path = os.path.join(dirpath, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    count = len(data) if isinstance(data, list) else 0
            except Exception:
                count = 0
            files.append((fname, count))
    return files


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return 'q'


def main():
    here = os.path.dirname(__file__)
    # Cargar varios bloques JSON en el orden especificado
    file_order = [
        'personas.json',
        'objetos_entornos.json',
        'alimentacion.json',
        'ciudad.json',
        'trabajo.json',
        'sociedad_naturaleza.json',
        'abstractos.json',
    ]

    for sel in file_order:
        path = os.path.join(here, sel)
        if not os.path.exists(path):
            print(f'No se encontró {sel} — se salta.')
            continue

        data = load_json(path)
        if not isinstance(data, list) or len(data) == 0:
            print(f'Archivo {sel} vacío o con formato incorrecto. Se salta.')
            continue

        # Aviso al cambiar de bloque
        bloque = os.path.splitext(sel)[0]
        print(f"\n\n=== Cambiando a bloque: {bloque} ===\n")

        for item in data:
            articulo = item.get('articulo', '').strip()
            singular = item.get('singular', '').strip()
            plural = item.get('plural', '').strip()
            traduccion = item.get('traduccion', '').strip()

            print('\n---')
            print(f"Alemán: {singular}  —  Español: {traduccion}")

            # artículo
            while True:
                ans = ask('Artículo > ')
                if ans.lower() == 'q':
                    print('Saliendo...')
                    return
                if ans.casefold() == articulo.casefold():
                    print('Artículo: correcto')
                    break
                else:
                    print('Artículo: incorrecto — inténtalo de nuevo')

            # plural
            if plural.lower() in ('n/a', 'na', '', 'none'):
                print('Nota: esta palabra no tiene plural.')
            else:
                while True:
                    ans = ask('Plural > ')
                    if ans.lower() == 'q':
                        print('Saliendo...')
                        return
                    if ans.casefold() == plural.casefold():
                        print('Plural: correcto')
                        break
                    else:
                        print('Plural: incorrecto — inténtalo de nuevo')
    print('\nFin del juego.')


if __name__ == '__main__':
    main()
