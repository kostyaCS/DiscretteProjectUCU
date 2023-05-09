from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path("register/", views.register, name="register"),
    path('user/', views.user_page, name='user_page'),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path('message/<str:pk>/', views.message, name='message'),
    path('chat_history/<str:pk>', views.chat_history, name='chat_history')
]
