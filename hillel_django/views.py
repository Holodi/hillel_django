from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from hillel_django import models
from hillel_django.models import Lesson, Word
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        # Перевірка на унікальність електронної пошти
        if User.objects.filter(email=email).exists():
            return HttpResponse('Ця електронна пошта вже використовується!')
        # Створення користувача
        User.objects.create_user(last_name=last_name, first_name=first_name, email=email, password=password)
        return HttpResponse('Користувач зареєстрований успішно!')
    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Перевірка введених даних
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Вхід успішний!')
        else:
            return HttpResponse('Неправильна електронна пошта або пароль!')
    return render(request, 'login.html')

@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        # Отримуємо дані форми з POST-запиту
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        # Отримуємо поточного користувача
        user.last_name = last_name
        user.first_name = first_name
        user.save()
        return redirect('user_profile')  # Перенаправляємо користувача на сторінку профілю
    return render(request, 'user_profile.html', {'user': user})

@login_required
def delete_user(request):
    if request.method == 'POST':
        # Отримуємо поточного користувача
        user = request.user
        # Видаляємо користувача
        user.delete()
        return redirect('login')  # Перенаправляємо користувача на сторінку входу
    else:
        # Повертаємо сторінку з підтвердженням видалення
        return render(request, 'delete_confirmation.html')

@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lesson_list.html', {'lessons': lessons})

@login_required
def lesson_detail(request, id):
    lesson = Lesson.objects.get(id=id)
    if request.method == 'POST':
        # Отримуємо дані результатів уроку з POST-запиту
        results = request.POST.getlist('results[]')
        # Логіка для збереження результатів уроку
        # Наприклад, ми можемо оновити атрибути уроку з результатами
        lesson.results = results
        lesson.save()
        return JsonResponse({'message': 'Результати уроку збережено успішно!'})
    else:
        return render(request, 'lesson_detail.html', {'lesson': lesson})

@login_required
def top_score(request):
    # Отримуємо список користувачів та сортуємо їх за сумою балів
    users = User.objects.annotate(total_score=models.Sum('lesson__result')).order_by('-total_score')
    return render(request, 'top_score.html', {'users': users})

@login_required
def word_list(request):
    # Отримуємо список слів поточного користувача
    user = request.user
    words = user.words.all()
    if request.method == 'POST':
        # Обробляємо додавання нового слова
        word = request.POST.get('word')
        translation = request.POST.get('translation')
        transliteration = request.POST.get('transliteration')
        phonetic_transcription = request.POST.get('phonetic_transcription')
        new_word = Word.objects.create(word=word, translation=translation, transliteration=transliteration, phonetic_transcription=phonetic_transcription, user=user)
        return redirect('word_list')
    return render(request, 'word_list.html', {'words': words})

@login_required
def word_detail(request, id):
    # Отримуємо деталі конкретного слова
    word = get_object_or_404(Word, id=id)
    if request.method == 'POST':
        # Обробляємо перевірку відповіді користувача
        answer = request.POST.get('answer')
        if answer.lower() == word.translation.lower():
            # Логіка для правильної відповіді
            messages.success(request, 'Правильна відповідь!')
        else:
            # Логіка для неправильної відповіді
            messages.error(request, 'Неправильна відповідь. Спробуйте ще раз.')
    return render(request, 'word_detail.html', {'word': word})