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
    sel = 'a1.json'
    path = os.path.join(here, sel)
    if not os.path.exists(path):
        print(f'No se encontró {sel} en el directorio.')
        return

    data = load_json(path)
    if not isinstance(data, list) or len(data) == 0:
        print('Archivo vacío o con formato incorrecto.')
        return

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
