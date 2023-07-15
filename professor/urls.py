from django.urls import path
from . import views

urlpatterns = [
    path('', views.professor_home, name='professor_home'),
    path('proctor/', views.proctor, name='proctor'),
    path('login/', views.professor_login, name='professor_login'),
    path('signup/', views.professor_signup, name='professor_signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('add_exam/', views.add_exam, name='add_exam'),
]
