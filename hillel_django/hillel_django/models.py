from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import AbstractUser, Group, Permission
from django import forms



class CustomUser(AbstractUser):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True)  # Додано related_name
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users', blank=True)  # Додано related_name

    class Meta:
        permissions = [
            ("custom_groups", "Can view custom groups"),
            ("custom_user_permissions", "Can view custom user permissions"),
        ]


class Lesson(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    results = models.JSONField(default=dict)


class Word(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    transliteration = models.CharField(max_length=100)
    phonetic_transcription = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_words')


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word', 'translation', 'transliteration', 'phonetic_transcription']
