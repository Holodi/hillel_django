from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from hillel_django.models import Lesson, Word, UserRegisterForm, UserLoginForm, WordForm, CustomUser  # Змінено імпорт


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
    return render(request, 'top_score.html', {'users': users})


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

