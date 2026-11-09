
from pathlib import Path

MAX_LINE_LENGTH = 120
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv"}


def check_file(file_path):
    errors = []

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if len(line.rstrip("\n\r")) > MAX_LINE_LENGTH:
                errors.append(
                    f"{file_path}:{line_number}: "
                    f"длина строки превышает {MAX_LINE_LENGTH} символов"
                )

    return errors


def main():
    errors = []

    for file_path in Path(".").rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue

        errors.extend(check_file(file_path))

    if errors:
        print("Обнаружены слишком длинные строки:")
        for error in errors:
            print(error)
        raise SystemExit(1)

    print("Проверка пройдена: все строки не длиннее 120 символов.")


if __name__ == "__main__":
    main()
