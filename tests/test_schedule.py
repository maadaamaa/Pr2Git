
# import unittest
# from schedule import filter_by_room


# class TestRoomFilter(unittest.TestCase):
#     def test_filters_lessons_by_room(self):
#         lessons = [
#             {
#                 "day": "Понедельник",
#                 "time": "09:00",
#                 "subject": "Python",
#                 "room": "301"
#             },
#             {
#                 "day": "Понедельник",
#                 "time": "10:00",
#                 "subject": "Математика",
#                 "room": "202"
#             }
#         ]

#         result = filter_by_room(lessons, "301")

#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["subject"], "Python")

#     def test_room_filter_ignores_case_and_spaces(self):
#         lessons = [
#             {
#                 "day": "Вторник",
#                 "time": "11:00",
#                 "subject": "Физика",
#                 "room": "301"
#             }
#         ]

#         self.assertEqual(len(filter_by_room(lessons, " 301 ")), 1)

#     def test_unknown_room_returns_empty_list(self):
#         self.assertEqual(
#             filter_by_room([], "999"),
#             []
#         )


# if __name__ == "__main__":
#     unittest.main()



import pytest
from schedule import add_lesson, has_overlap


@pytest.fixture
def lessons():
    return [
        {
            "day": "Понедельник",
            "start": "08:00",
            "end": "09:30",
            "subject": "Математика",
            "room": "101"
        }
    ]


def test_overlap_is_rejected(lessons, monkeypatch):
    monkeypatch.setattr("schedule.save_schedule", lambda data: None)

    result = add_lesson(
        lessons,
        "Понедельник",
        "09:00",
        "10:00",
        "Физика",
        "102"
    )

    assert result is False
    assert len(lessons) == 1


def test_non_overlapping_is_accepted(lessons, monkeypatch):
    monkeypatch.setattr("schedule.save_schedule", lambda data: None)

    result = add_lesson(
        lessons,
        "Понедельник",
        "09:30",
        "10:30",
        "Физика",
        "102"
    )

    assert result is True
    assert len(lessons) == 2


def test_overlap_function():
    assert has_overlap("08:00", "09:30", "09:00", "10:00")


def test_no_overlap_function():
    assert not has_overlap("08:00", "09:30", "09:30", "10:30")


def test_invalid_time(lessons):
    result = add_lesson(
        lessons,
        "Понедельник",
        "неверно",
        "10:00",
        "Физика",
        "102"
    )

    assert result is False
    assert len(lessons) == 1


def test_end_before_start(lessons):
    result = add_lesson(
        lessons,
        "Понедельник",
        "11:00",
        "10:00",
        "Физика",
        "102"
    )

    assert result is False
    assert len(lessons) == 1


def test_different_day_is_accepted(lessons, monkeypatch):
    monkeypatch.setattr("schedule.save_schedule", lambda data: None)

    result = add_lesson(
        lessons,
        "Вторник",
        "08:00",
        "09:00",
        "Физика",
        "102"
    )

    assert result is True
    assert len(lessons) == 2


def test_different_room_same_time_is_rejected(lessons):
    result = add_lesson(
        lessons,
        "Понедельник",
        "08:30",
        "09:00",
        "Физика",
        "102"
    )

    assert result is False
    assert len(lessons) == 1


def test_same_room_different_time_is_accepted(lessons, monkeypatch):
    monkeypatch.setattr("schedule.save_schedule", lambda data: None)

    result = add_lesson(
        lessons,
        "Понедельник",
        "10:00",
        "11:00",
        "Физика",
        "101"
    )

    assert result is True
    assert len(lessons) == 2


def test_touching_intervals_are_accepted(lessons, monkeypatch):
    monkeypatch.setattr("schedule.save_schedule", lambda data: None)

    result = add_lesson(
        lessons,
        "Понедельник",
        "09:30",
        "10:30",
        "Физика",
        "101"
    )

    assert result is True
    assert len(lessons) == 2
