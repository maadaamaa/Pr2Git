
import json
from datetime import datetime
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
        raise ValueError(
            f"Некорректный DAY_START: {day_start!r}. "
            "Ожидается целое число от 0 до 23."
        )

    return config

def load_schedule():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_schedule(lessons):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(lessons, file, ensure_ascii=False, indent=2)

def has_overlap(start1, end1, start2, end2):
    start1 = datetime.strptime(start1, "%H:%M")
    end1 = datetime.strptime(end1, "%H:%M")
    start2 = datetime.strptime(start2, "%H:%M")
    end2 = datetime.strptime(end2, "%H:%M")

    return start1 < end2 and start2 < end1


def add_lesson(lessons, day, start, end, subject, room):
    try:
        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")
    except ValueError:
        print("Ошибка: время должно быть в формате ЧЧ:ММ.")
        return False

    if start_time >= end_time:
        print("Ошибка: время окончания должно быть позже начала.")
        return False

    for lesson in lessons:
        if lesson["day"].lower() != day.lower():
            continue

        if has_overlap(
            start,
            end,
            lesson["start"],
            lesson["end"]
        ):
            print("Ошибка: время занятия пересекается с другим занятием.")
            return False

        # if lesson["room"].strip().lower() == room.strip().lower():
        #     print("Ошибка: аудитория уже занята.")
        #     return False

    lesson = {
        "day": day,
        "start": start,
        "end": end,
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

    day_lessons.sort(key=lambda lesson: lesson["start"])    
    if not day_lessons:
        print(f"На день «{day}» занятий нет.")
        return

    print(f"Расписание на день: {day}")
    for lesson in day_lessons:
        print(
            f'{lesson["start"]}-{lesson["end"]} | {lesson["subject"]} '
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
