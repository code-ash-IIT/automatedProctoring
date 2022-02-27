from django.urls import include, path
from. import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index),
    path('cllogin', views.cllogin),
    path('clsignup', views.clsignup),
    path('signup', views.signup),
    path('login', views.userlogin),
    path('logout', views.userlogout),
]

urlpatterns+=staticfiles_urlpatterns()