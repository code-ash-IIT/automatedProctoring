from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.student_home, name='student_home'),
    path('exam/', views.student_exam, name='student_exam'),
    path('login/', views.student_login, name='student_login'),
    path('signup/', views.student_signup, name='student_signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('exam-submission-confirmation/', views.exam_submission_confirmation, name='exam_submission_confirmation'),
]
