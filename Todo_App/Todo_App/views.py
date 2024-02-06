from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # For user, create, read
from django.contrib import messages  # For display the alert messages
from datetime import datetime


def index(request):
    # return HttpResponse("Hello")
    return render(request, 'todo/index.html')


def register(request):
    if request.method == "POST":
        f_name = request.POST.get('f_name', '')
        l_name = request.POST.get('l_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('u_name', '')
        password = request.POST.get('pass', '')
        dob = request.POST.get('dob', '')

        # Convert DOB to datetime object
        dob = datetime.strptime(dob, '%Y-%m-%d').date() if dob else None

        # Check For Unique User_Name
        if User.objects.filter(username=username):
            messages.error(request, "Your Provided User Name is Already Exists, Please Try With Different User Name.")
            return redirect('register')

        # Create User
        user = User.objects.create_user(username, email, password)
        # Add Additional Information
        user.first_name = f_name
        user.last_name = l_name
        user.date_of_birth = dob  # Set DOB
        # Initially this user account will Deactivate
        # After email verification it will be Active
        user.is_active = False
        user.save()

        # Success Messages
        messages.success(request, "Congratulations, Your Account Created Successfully.Please Check your email, "
                                  "and verified you account.")
        return redirect('register')
        # print(f_name, l_name, email, username, password, dob)

    return render(request, 'todo/register.html')


def login(request):
    if request.method == "POST":
        uname = request.POST.get('u_name', '')
        password = request.POST.get('pass', '')

        print(uname, password)
    return render(request, 'todo/login.html')


def logout(request):
    pass
