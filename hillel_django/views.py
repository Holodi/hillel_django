from random import shuffle
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from hillel_django.models import Lesson, Word, UserRegisterForm, UserLoginForm, WordForm, CustomUser, AnswerForm


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Користувач зареєстрований успішно!')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('Вхід успішний!')
            else:
                return HttpResponse('Неправильна електронна пошта або пароль!')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено успішно!')
            return redirect('user_profile')
    else:
        form = UserRegisterForm(instance=user)
    return render(request, 'user_profile.html', {'form': form})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('login')
    else:
        return render(request, 'delete_confirmation.html')

@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lesson_list.html', {'lessons': lessons})

@login_required
def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    if request.method == 'POST':
        results = request.POST.getlist('results[]')
        lesson.results = results
        lesson.save()
        return JsonResponse({'message': 'Результати уроку збережено успішно!'})
    else:
        return render(request, 'lesson_detail.html', {'lesson': lesson})

@login_required
def top_score(request):
    users = CustomUser.objects.annotate(total_score=Sum('lesson__result')).order_by('-total_score')
    return render(request, 'leaderboard.html', {'users': users})

@login_required
def word_list(request):
    user = request.user
    words = user.user_words.all()
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = user
            word.save()
            return redirect('word_list')
    else:
        form = WordForm()
    return render(request, 'word_list.html', {'words': words, 'form': form})


@login_required
def word_detail(request, id):
    word = get_object_or_404(Word, id=id)
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer.lower() == word.translation.lower():
            messages.success(request, 'Правильна відповідь!')
        else:
            messages.error(request, 'Неправильна відповідь. Спробуйте ще раз.')
    return render(request, 'word_detail.html', {'word': word})

@login_required
def random_words(request):
    # Отримання списку всіх слів та перемішування їх
    words = list(Word.objects.all())
    shuffle(words)
    # Передача перемішаного списку слів на сторінку
    return render(request, 'random_words.html', {'words': words})

@login_required
def check_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            word_id = form.cleaned_data['word_id']
            answer = form.cleaned_data['answer']
            word = get_object_or_404(Word, id=word_id)
            if answer.lower() == word.translation.lower():
                # Логіка для успішної відповіді
                request.user.score += 1
                request.user.save()
                messages.success(request, 'Правильна відповідь! Бали додано.')
            else:
                messages.error(request, 'Неправильна відповідь. Спробуйте ще раз.')
            return redirect('word_detail', id=word_id)
    else:
        form = AnswerForm()
    return render(request, 'check_answer.html', {'form': form})


@login_required
def lesson_list(request):
    # Отримання списку усіх занять
    lessons = Lesson.objects.all()
    return render(request, 'lesson_list.html', {'lessons': lessons})

@login_required
def lesson_detail(request, lesson_id):
    # Отримання детальної інформації про конкретне заняття
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            # Логіка перевірки відповіді
            user_answer = form.cleaned_data['answer']
            correct_answer = lesson.correct_answer
            if user_answer.lower() == correct_answer.lower():
                message = 'Правильна відповідь!'
            else:
                message = 'Неправильна відповідь. Спробуйте ще раз.'
            return render(request, 'lesson_result.html', {'message': message})
    else:
        form = AnswerForm()
    return render(request, 'lesson_detail.html', {'lesson': lesson, 'form': form})

def finish_lesson(request):
    if request.method == 'POST':
        # Отримання результатів уроку з форми або request.POST
        results = request.POST.getlist('results[]')
        # Оновлення балів користувача після завершення урока
        request.user.score += len(results)
        request.user.save()
        messages.success(request, 'Урок завершено. Бали додано.')
        return render(request, 'finish_lesson.html')  # Перенаправлення на сторінку завершення уроку
    else:
        messages.error(request, 'Неможливо завершити урок. Невірний метод запиту.')
        return redirect('lesson_list')  # Перенаправлення на список уроків