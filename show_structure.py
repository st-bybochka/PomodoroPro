import os
from pathlib import Path


def print_structure(startpath, max_level=3, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = ['.venv', '__pycache__', '.git']

    startpath = Path(startpath)
    print(f"{startpath.name}/")

    for root, dirs, files in os.walk(startpath):
        # Фильтрация исключенных папок
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = Path(root).relative_to(startpath).parts
        if len(level) > max_level:
            continue

        indent = '    ' * len(level)
        # Выводим только имя текущей директории (не полный путь)
        print(f"{indent}{Path(root).name}/")

        # Выводим файлы
        subindent = '    ' * (len(level) + 1)
        for f in sorted(files):
            # Пропускаем служебные файлы
            if not f.endswith(('.py', '.md', '.txt', '.ini', '.env')):
                continue
            print(f"{subindent}{f}")



print_structure(Path(__file__).parent, max_level=4)