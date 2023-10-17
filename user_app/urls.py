from django.urls import path
from . import views

urlpatterns = [

    path('register', views.registerPage, name="register"),
    path('registerUser', views.registerUser, name="registerUser"),
    path('login', views.loginPage, name="login"),
    path('loginUser', views.loginUser, name="loginUser"),
    path('logout', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('api', views.api, name="api"),
]