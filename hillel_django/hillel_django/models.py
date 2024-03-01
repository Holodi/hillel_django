from django.db import models


class User(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


class Lesson(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    results = models.JSONField(default=dict)


class Word(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    transliteration = models.CharField(max_length=100)
    phonetic_transcription = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='words')
