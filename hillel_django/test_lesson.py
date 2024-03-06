from django.test import TestCase, Client
from django.urls import reverse
from hillel_django.models import Lesson

class LessonViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Description')

    def test_lesson_list(self):
        response = self.client.get(reverse('lesson_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_list.html')

    def test_lesson_detail(self):
        response = self.client.get(reverse('lesson_detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_detail.html')

    def test_top_score(self):
        response = self.client.get(reverse('top_score'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard.html')
