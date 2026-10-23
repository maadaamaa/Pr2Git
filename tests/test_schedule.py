
import unittest
from schedule import filter_by_room


class TestRoomFilter(unittest.TestCase):
    def test_filters_lessons_by_room(self):
        lessons = [
            {
                "day": "Понедельник",
                "time": "09:00",
                "subject": "Python",
                "room": "301"
            },
            {
                "day": "Понедельник",
                "time": "10:00",
                "subject": "Математика",
                "room": "202"
            }
        ]

        result = filter_by_room(lessons, "301")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["subject"], "Python")

    def test_room_filter_ignores_case_and_spaces(self):
        lessons = [
            {
                "day": "Вторник",
                "time": "11:00",
                "subject": "Физика",
                "room": "301"
            }
        ]

        self.assertEqual(len(filter_by_room(lessons, " 301 ")), 1)

    def test_unknown_room_returns_empty_list(self):
        self.assertEqual(
            filter_by_room([], "999"),
            []
        )


if __name__ == "__main__":
    unittest.main()
