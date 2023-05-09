"""
This module includes all views in application.
"""
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, MessageForm
from .models import User, Message, MessageHistory
from django.contrib.auth.models import User
from django.db.models import Q


def main_page(request):
    """
    This method is a views for main page when user visit web application.
    """
    return render(request, 'message_app/main.html', {})


def register(request):
    """
    This method is a view for user's registration.
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user_page")
    form = NewUserForm()
    return render(request=request, template_name="message_app/register.html",\
                   context={"register_form":form})


def login_user(request):
    """
    This method is a view for user's loginization and authentication.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("user_page")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="message_app/login.html",\
                  context={"login_form":form})


def logout_request(request):
    """
    This method do a user's logout from account.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('register')


@login_required
def user_page(request):
    """
    This method is a view for user's main page.
    """
    if request.method == "POST":
        if 'search' in request.POST:
            return redirect(message, pk=request.POST['name'])
        elif 'history' in request.POST:
            return redirect(chat_history, pk=request.user)
    user = request.user
    context = {
    'username': user.username,
    'email': user.email,
    }
    return render(request, 'message_app/user_page.html', context)


@login_required
def message(request, pk=None):
    """
    This method helps user to see all the messages and to send new one.
    """
    if pk:
        receiver = get_object_or_404(User, username=pk)
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                message = Message.objects.create(sender=request.user, receiver=receiver, text=text)
                if request.user == message.sender and receiver == message.receiver:
                    MessageHistory.objects.create(user=request.user, message=message)
                    MessageHistory.objects.create(user=receiver, message=message)
                return redirect('message', pk=pk)
        else:
            form = MessageForm()
        messages = MessageHistory.objects.filter(
    Q(user=request.user, message__sender=request.user, message__receiver=receiver) | 
    Q(user=request.user, message__sender=receiver, message__receiver=request.user)
    ).order_by('date')
        context = {'form': form, 'messages': messages, 'receiver': receiver}
        return render(request, 'message_app/message.html', context)
    else:
        messages = MessageHistory.objects.filter(user=request.user).order_by('-date')
        context = {'messages': messages}
        return render(request, 'message_app/message_history.html', context)


def chat_history(request, pk=None):
    """
    This method show user's chat history.
    """
    user = get_object_or_404(User, username=pk)
    set_with_results = set()
    for i in MessageHistory.objects.filter(user=user.id):
        if str(i.message.receiver) != request.user.username:
            set_with_results.add(i.message.receiver)
    return render(request, 'message_app/message_history.html', {'user':set_with_results})
