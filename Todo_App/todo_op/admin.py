from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import TodoList

admin.site.register(TodoList)

