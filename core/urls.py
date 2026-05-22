from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),

    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add/', views.add_complaint, name='add_complaint'),

    path('view/', views.view_complaints, name='view_complaints'),

    path('delete/<int:id>/',
         views.delete_complaint,
         name='delete_complaint'),

    path('logout/', views.user_logout, name='logout'),

]