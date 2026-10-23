
import json
from pathlib import Path

DATA_FILE = Path("schedule.json")


def load_schedule():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_schedule(lessons):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(lessons, file, ensure_ascii=False, indent=2)


def main():
    lessons = load_schedule()
    print(f"Занятий в расписании: {len(lessons)}")


if __name__ == "__main__":
    main()
