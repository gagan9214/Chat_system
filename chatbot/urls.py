from django.urls import path
from chatbot import views

urlpatterns = [
    path("",views.loginPage,name='loginPage'),
    path("signup/",views.signupPage, name='signupPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('chat/', views.chat, name='chat'),
    path('home/', views.home, name='home'),
    
]
