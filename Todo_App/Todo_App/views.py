from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    # return HttpResponse("Hello")
    return render(request, 'todo/index.html')


def register(request):
    if request.method == "POST":
        f_name = request.POST.get('f_name', '')
        l_name = request.POST.get('l_name', '')
        email = request.POST.get('email', '')
        uname = request.POST.get('u_name', '')
        password = request.POST.get('pass', '')
        dob = request.POST.get('dob', '')

        print(f_name, l_name, email, uname, password, dob)

    return render(request, 'todo/register.html')


def login(request):
    if request.method == "POST":
        uname = request.POST.get('u_name', '')
        password = request.POST.get('pass', '')

        print(uname, password)
    return render(request, 'todo/login.html')


def logout(request):
    pass