from django.test import TestCase
from .scoring import calculate_score
from datetime import date, timedelta

class ScoreTests(TestCase):

    def test_score_calculation(self):
        """
        Test basic score calculation for a normal task
        """
        t = {
            "title": "Test Task",
            "due_date": date.today(),
            "estimated_hours": 3,
            "importance": 8,
            "dependencies": []
        }
        tasks = [t]
        score, _ = calculate_score(t, tasks)
        # Minimum expected score based on weights
        self.assertTrue(score > 5)

    def test_fastest_strategy(self):
        """
        Test that 'fastest' strategy favors low-effort tasks
        """
        t = {
            "title": "Fast Task",
            "due_date": date.today(),
            "estimated_hours": 1,
            "importance": 5,
            "dependencies": []
        }
        tasks = [t]
        score, _ = calculate_score(t, tasks, "fastest")
        # Fast task should score reasonably high
        self.assertTrue(score > 6)

    def test_overdue_priority(self):
        """
        Test that overdue tasks have high urgency score
        """
        t = {
            "title": "Late Task",
            "due_date": date.today() - timedelta(days=2),
            "estimated_hours": 4,
            "importance": 5,
            "dependencies": []
        }
        tasks = [t]
        score, _ = calculate_score(t, tasks)
        # Current weights result in score around 6.7
        self.assertTrue(score > 6)
