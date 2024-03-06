from django.test import TestCase, Client
from django.urls import reverse
from hillel_django.models import Word

class WordViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.word = Word.objects.create(word='Test Word', translation='Test Translation')

    def test_word_list(self):
        response = self.client.get(reverse('word_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word_list.html')

    def test_word_detail(self):
        response = self.client.get(reverse('word_detail', args=[self.word.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word_detail.html')

    def test_random_words(self):
        response = self.client.get(reverse('random_words'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'random_words.html')

    def test_check_answer(self):
        response = self.client.get(reverse('check_answer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check_answer.html')