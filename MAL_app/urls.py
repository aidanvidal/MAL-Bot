from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_screen, name='login_screen'),
    path('login/', views.login_screen, name='login_screen'),
    path('home/', views.home, name='home'),
    path('token/', views.token, name='token'),
    path('create/', views.create, name='create'),
    path('process_input/', views.process_input, name='process_input'),
    path('logout/', views.logout_view, name='logout_view'),
    path('generate_token_link/', views.generate_token_link, name='generate_token_link'),
]