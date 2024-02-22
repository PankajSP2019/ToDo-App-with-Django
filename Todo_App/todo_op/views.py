import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # For user, create, read
from django.contrib import messages  # For display the alert messages
from django.contrib.auth import authenticate, login, logout  # For login, logout
from django.contrib.auth.decorators import login_required  # For ensure, user is logged in
from datetime import datetime
# For sending email, and verified email
from django.conf import settings
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str  # force_text

# Import Models
from .models import TodoList


def index(request):
    # return HttpResponse("Hello")
    return render(request, 'todo_op/index.html')


def register(request):
    # If the user already logged in , user cannot go to register page
    if request.user.is_authenticated:
        return redirect('content', u_name=request.user.username)

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

        # Welcome Email
        subject = "Welcome To To-Do APP!!"
        message = f"Hello {user.first_name}!!\n\nWelcome to a freshly launched To-Do app. We have also sent you a confirmation email, please confirm your email address. \n\nThank You\nPankaj Kumar Das\nDeveloper - To-Do App"
        from_email = settings.EMAIL_HOST_USER
        to_email_list = [user.email]
        send_mail(subject, message, from_email, to_email_list, fail_silently=True)

        # Email Address Confirmation
        # Send an email with a link and after clicking the link address, the user will be active
        current_site = get_current_site(request)
        email_subject = "Confirmation Email TO Logged In To-Do App"
        c_message = render_to_string('todo_op/email_confirmation.html', {
            'name': user.first_name,
            'domain': current_site.domain,  # Get The domain like 127.0.0.1:8000 -> using it
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,
            c_message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()

        # Success Messages
        messages.success(request, "Congratulations, Your Account Created Successfully.Please Check your email, "
                                  "and verified you account.")
        return redirect('register')
        # print(f_name, l_name, email, username, password, dob)

    return render(request, 'todo_op/register.html')


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    # except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        # user.profile.signup_confirmation = True
        user.save()
        # login(request, user)
        messages.success(request,
                         "Your Account is activate Now. Please Login in with your username and password Thanks For being with us!!")
        return redirect('login')
    else:
        return HttpResponse(f"Something Went wrong, Please Inform Our Admin.")


def login_todo(request):
    # If the user already logged in , user cannot go to register page
    if request.user.is_authenticated:
        return redirect('content', u_name=request.user.username)

    if request.method == "POST":
        uname = request.POST.get('u_name', '')
        password = request.POST.get('pass', '')

        # It will check the username and password
        user = authenticate(username=uname, password=password)
        if user is not None:
            login(request, user)
            f_name = user.first_name
            l_name = user.last_name
            data = {'f_name': f_name, 'l_name': l_name}
            return redirect('content', u_name=user.username)
        else:
            messages.error(request, "Wrong User and Password")
            return redirect('login')

    return render(request, 'todo_op/login.html')


# I face problem when I run this in Chrome browser,
# After clear the cached image and file and cookies, it's running well
@login_required(login_url='/todo/login/')
def show_content(request, u_name):
    # Fetch the data in descending order that's why put '-' before the field name
    all_data = TodoList.objects.filter(user_name=request.user.username).order_by('-todo_id')

    # Count the number of pending updates
    pending_count = all_data.filter(status='pending').count()

    return render(request, 'todo_op/content.html', {'content': all_data, 'pending_count': pending_count})


@login_required(login_url='/todo/login/')
def add_todo(request):
    if request.method == "POST":
        t_title = request.POST.get('t_title', '').title()
        t_description = request.POST['t_description']  # we collect the value from textarea field
        try:
            new = TodoList(user_name=request.user.username, title=t_title, content=t_description, status="pending")
            new.save()

            # Return new Content
            # Fetch the data in descending order that's why put '-' before the field name
            all_data = TodoList.objects.filter(user_name=request.user.username).order_by('-todo_id')
            if len(all_data) > 0:
                update_data = []
                for i in all_data:
                    update_data.append(
                        {'title': i.title, 'todo_id': i.todo_id, 'content': i.content, 'status': i.status})
                    response = json.dumps([update_data], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            print(e)
            return HttpResponse('{}')


@login_required(login_url='/todo/login/')
def done_todo(request):
    if request.method == "POST":
        tid = request.POST.get('todo_id', '')
        tid = int(tid)

        try:
            # Update the status of to-do item
            done = TodoList.objects.filter(user_name=request.user.username, todo_id=tid)
            done.update(status="done")

            # Return new Content
            # Fetch the data in descending order that's why put '-' before the field name
            all_data = TodoList.objects.filter(user_name=request.user.username).order_by('-todo_id')
            if len(all_data) > 0:
                update_data = []
                for i in all_data:
                    update_data.append({'title': i.title,'todo_id': i.todo_id, 'content': i.content, 'status': i.status})
                    response = json.dumps([update_data], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            print(e)
            return HttpResponse(e)


@login_required(login_url='/todo/login/')
def delete_todo(request):
    if request.method == "POST":
        tid = request.POST.get('todo_id', '')
        tid = int(tid)

        try:
            # Delete the to-do item
            done = TodoList.objects.filter(user_name=request.user.username, todo_id=tid)
            done.delete()

            # Return new Content
            # Fetch the data in descending order that's why put '-' before the field name
            all_data = TodoList.objects.filter(user_name=request.user.username).order_by('-todo_id')
            if len(all_data) > 0:
                update_data = []
                for i in all_data:
                    update_data.append(
                        {'title': i.title, 'todo_id': i.todo_id, 'content': i.content, 'status': i.status})
                    response = json.dumps([update_data], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            print(e)
            return HttpResponse(e)


@login_required(login_url='/todo/login/')
def logout_todo(request):
    logout(request)
    messages.success(request, "Successfully Logged out, Thank you")
    return redirect('login')


# for check login in views if request.user.is_authenticated:
# for check login in templates {% if user.is_authenticated %}


def check(request):
    return HttpResponse("Check Done")
