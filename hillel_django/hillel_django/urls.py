from django.contrib import admin
from django.urls import path
import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('user/', views.user_profile, name='user'),
    path('user/delete/', views.delete_user, name='delete_user'),
    path('lesson/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('top_score/', views.top_score, name='top_score'),
    path('words/', views.word_list, name='word_list'),
    path('words/<int:id>/', views.word_detail, name='word_detail'),
]
