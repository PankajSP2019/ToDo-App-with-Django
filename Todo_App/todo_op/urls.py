from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('check/', views.check, name="check"),
    path("", views.index, name="homepage"),
    path("register/", views.register, name="register"),
    path("login/", views.login_todo, name="login"),
    path("content/<str:u_name>", views.show_content, name="content"),  # pass with username
    path("logout/", views.logout_todo, name="logout"),
    path('activate/<uidb64>/<token>', views.activate_user, name='activate'),
    path('addtodo/', views.add_todo, name='add_todo'),
    path('done_todo/', views.done_todo, name='done_todo'),
    path('delete_todo/', views.delete_todo, name='delete_todo'),

]
