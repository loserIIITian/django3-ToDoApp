from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Todo
from django.utils import timezone
from .forms import TodoForm, CreateUserForm
from email.message import EmailMessage
import smtplib


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'notes/signupuser.html', {'form': CreateUserForm()})
    else:

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'], first_name = request.POST['first_name'], email=request.POST['email'])
                user.save()
                login(request, user)
                # simple mail transfer protocol library
                # start  session
                msg = EmailMessage()
                msg.set_content(
                    'Dear ' + request.user.username + ','
                                                      '\nWelcome to Schedule.It.\nWe are glad to have you aboard. Keep crushing tasks and keep updating them at scheduleIT.pythonanywhere.com.')
                msg['Subject'] = 'Thank you for registering'
                msg['From'] = "your.schedule.it@gmail.com"
                msg['To'] = request.user.email
                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("your.schedule.it@gmail.com", "jesuisiamajit")
                server.send_message(msg)
                server.quit()
                # send e-mail. keep google api file in directory
                return redirect('currenttodos')
            except IntegrityError:

                return render(request, 'notes/signupuser.html', {'form': CreateUserForm(),
                                                                 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'notes/signupuser.html',
                          {'form': CreateUserForm(), 'error': 'Passwords did not match. Please try again'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'notes/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'notes/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True).count()
            if todos > 5:
                # simple mail transfer protocol library
                # start  session

                msg = EmailMessage()
                msg.set_content(
                    'Dear ' + request.user.username + '\nYou have ' + str(todos) + ' remaining to-dos.\nYou just added ' + newtodo.title + '\n Make sure to finish them and reach your goals!!\n\nKeep crushing tasks and update them at scheduleIT.pythonanywhere.com.')
                msg['Subject'] = str(todos) + ' To-dos left to complete !'
                msg['From'] = "your.schedule.it@gmail.com"
                msg['To'] = request.user.email
                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("your.schedule.it@gmail.com", "jesuisiamajit")
                server.send_message(msg)
                server.quit()
                # send e-mail. keep google api file in directory
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')
    else:
        return redirect('currenttodos')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'notes/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True).count()
            mail = 0
            if todos > 5:
                # simple mail transfer protocol library
                # start  session
                msg = EmailMessage()
                msg.set_content(
                    'Dear ' + request.user.username + '\nYou have ' + str(todos) + ' remaining to-dos.\nYou just added ' + newtodo.title + '\n Make sure to finish them and reach your goals!!\n\nKeep crushing tasks and update them at scheduleIT.pythonanywhere.com.')
                msg['Subject'] = str(todos) + ' To-dos left to complete !'
                msg['From'] = "your.schedule.it@gmail.com"
                msg['To'] = request.user.email
                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("your.schedule.it@gmail.com", "jesuisiamajit")
                server.send_message(msg)
                server.quit()
                mail = 1
                # send e-mail. keep google api file in directory
            if newtodo.important and mail == 0:
                # simple mail transfer protocol library
                # start  session
                msg = EmailMessage()
                msg.set_content(
                    'Dear ' + request.user.username + '.\nYou have added an important note. ' + newtodo.title + '\nCrush the task and visit us back!')
                msg['Subject'] = 'You added an important note on Schedule.It'
                msg['From'] = "your.schedule.it@gmail.com"
                to = request.user.email
                msg['To'] = to
                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("your.schedule.it@gmail.com", "jesuisiamajit")
                server.send_message(msg)
                server.quit()
                # send e-mail. keep google api file in directory
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'notes/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'notes/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'notes/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'notes/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            newtodo = form.save(commit=False)
            if newtodo.important:
                # simple mail transfer protocol library
                # start  session
                msg = EmailMessage()
                msg.set_content(
                    'Dear' + request.user.username + ' you have added an important note. ' + newtodo.title + ' Crush the task and visit us back!\n\nKeep crushing tasks and update them at scheduleIT.pythonanywhere.com.')
                msg['Subject'] = 'You updated an important note on Schedule.It'
                msg['From'] = "your.schedule.it@gmail.com"
                msg['To'] = request.user.email
                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("your.schedule.it@gmail.com", "jesuisiamajit")
                server.send_message(msg)
                server.quit()
                # send e-mail. keep google api file in directory
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})

            return redirect('currenttodos')
        except ValueError:
            return render(request, 'notes/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
