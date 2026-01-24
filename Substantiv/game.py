#!/usr/bin/env python3
import os
import json
import random


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
    files = list_json_files(here)
    if not files:
        print('No hay archivos JSON en el directorio.')
        return

    print('Elige un archivo de sustantivos:')
    for i, (name, count) in enumerate(files, 1):
        print(f"{i}. {name} ({count} palabras)")

    choice = ask("Número o nombre (o 'q' para salir): ")
    if choice.lower() == 'q':
        print('Fin del juego.')
        return

    sel = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            sel = files[idx][0]
    else:
        for name, count in files:
            if name == choice:
                sel = name
                break

    if not sel:
        print('Selección inválida.')
        return

    data = load_json(os.path.join(here, sel))
    if not isinstance(data, list) or len(data) == 0:
        print('Archivo vacío o con formato incorrecto.')
        return

    shuffle = ask("Aleatorizar orden? (s/n) [n]: ").lower() in ('s', 'si', 'y', 'yes')
    if shuffle:
        random.shuffle(data)

    for item in data:
        articulo = item.get('articulo', '').strip()
        singular = item.get('singular', '').strip()
        plural = item.get('plural', '').strip()
        traduccion = item.get('traduccion', '').strip()

        print('\n---')
        print(f"Alemán: {singular}  —  Español: {traduccion}")

        # artículo
        ans = ask('Artículo > ')
        if ans.lower() == 'q':
            break
        if ans.casefold() == articulo.casefold():
            print('Artículo: correcto')
        else:
            print(f'Artículo: incorrecto — respuesta: {articulo}')
        # (No se pide el singular; ya aparece en el enunciado)

        # plural
        if plural.lower() in ('n/a', 'na', '', 'none'):
            print('Nota: esta palabra no tiene plural. No introduzcas plural.')
        else:
            ans = ask('Plural > ')
            if ans.lower() == 'q':
                break
            if ans.casefold() == plural.casefold():
                print('Plural: correcto')
            else:
                print(f'Plural: incorrecto — respuesta: {plural}')
    print('\nFin del juego.')


if __name__ == '__main__':
    main()
