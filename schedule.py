
import json
from pathlib import Path

DATA_FILE = Path("schedule.json")

CONFIG_FILE = Path("config.json")

def load_config():
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    else:
        config = {"DAY_START": 8}

    day_start = config.get("DAY_START")

    if type(day_start) is not int or not 0 <= day_start <= 23:
        raise ValueError("DAY_START должен быть целым числом от 0 до 23")

    return config

def load_schedule():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_schedule(lessons):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(lessons, file, ensure_ascii=False, indent=2)



def add_lesson(lessons, day, time, subject, room):
    for lesson in lessons:
        if (
            lesson["day"] == day
            and lesson["time"] == time
            and lesson["room"] == room
        ):
            print("Ошибка: аудитория уже занята в это время.")
            return False

    lesson = {
        "day": day,
        "time": time,
        "subject": subject,
        "room": room
    }
    lessons.append(lesson)
    save_schedule(lessons)
    print("Занятие добавлено.")
    return True


def show_day(lessons, day):
    day_lessons = [
        lesson for lesson in lessons
        if lesson["day"].lower() == day.lower()
    ]

    day_lessons.sort(key=lambda lesson: lesson["time"])

    if not day_lessons:
        print(f"На день «{day}» занятий нет.")
        return

    print(f"Расписание на день: {day}")
    for lesson in day_lessons:
        print(
            f'{lesson["time"]} | {lesson["subject"]} '
            f'| аудитория {lesson["room"]}'
        )


def filter_by_room(lessons, room):
    return [
        lesson for lesson in lessons
        if lesson["room"].strip().lower() == room.strip().lower()
    ]


def main():
    lessons = load_schedule()
    print(f"Занятий в расписании: {len(lessons)}")


if __name__ == "__main__":
    main()
