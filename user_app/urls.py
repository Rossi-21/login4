from django.urls import path
from . import views

urlpatterns = [

    path('register', views.registerPage, name="register"),
    path('registerUser', views.registerUser, name="registerUser"),
    path('login', views.loginPage, name="login"),
    path('loginUser', views.loginUser, name="loginUser"),
    path('', views.home, name="home"),
    #path('logout/', views.logoutUser, name="logout"),
]