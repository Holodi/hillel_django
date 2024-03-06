from django.test import TestCase, Client
from django.urls import reverse
from hillel_django.models import CustomUser, Lesson

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password')

    def test_register_user(self):
        response = self.client.post(reverse('register_user'), {'email': 'test@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Користувач зареєстрований успішно!', response.content)

    def test_login_user(self):
        response = self.client.post(reverse('login_user'), {'email': 'test@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Вхід успішний!', response.content)

    def test_user_profile(self):
        self.client.login(email='test@example.com', password='password')
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')

    def test_delete_user(self):
        self.client.login(email='test@example.com', password='password')
        response = self.client.post(reverse('delete_user'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomUser.objects.filter(email='test@example.com').exists())