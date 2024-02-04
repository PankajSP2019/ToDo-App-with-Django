from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    # return HttpResponse("Hello")
    return render(request, 'todo/index.html')
