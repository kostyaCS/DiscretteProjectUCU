"""
This module includes all views in application.
"""
from functools import lru_cache
import base64
from django import forms
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, MessageForm
from .models import User, Message, MessageHistory, UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
import json
from PIL import Image
from io import BytesIO
from django.http import HttpResponse

def greeting(request):
    """
    This method is a views for main page when user visit web application.
    """
    if request.method == 'POST':
        return redirect('register')
    return render(request, 'message_app/start_page.html', {})

def register(request):
    """
    This method is a view for user's registration.
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(user=user)
            profile.save()
            login(request, user)
            profile.save()
            return redirect(chat_history, pk=request.user)
    else:
        form = NewUserForm()
    return render(request=request, template_name="message_app/register.html", context={"register_form": form})

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
                return redirect(chat_history, pk=request.user)
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
        if 'history' in request.POST:
            return redirect(chat_history, pk=request.user)
        elif 'delete' in request.POST:
            user = User.objects.get(username=request.user.username)
            user.delete()
            return redirect('/')
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    context = {
    'username': user.username,
    'email': user.email,
    'key': user_profile.rb.n_var
    }
    return render(request, 'message_app/user_page.html', context)

@lru_cache
@login_required
def message(request, pk=None):
    """
    This method helps user to see all the messages and to send new one.
    """
    is_send_visible = False
    if pk:
        receiver = get_object_or_404(User, username=pk)
        profile_of_receiver = UserProfile(user=receiver)
        profile_of_sender = UserProfile(user=request.user)
        if request.method == 'POST':
            form = MessageForm(request.POST, request.FILES)
            if form.is_valid():
                text = form.cleaned_data['text']
                text = profile_of_receiver.rb.encode(profile_of_receiver.rb.n_var, text)
                image = form.cleaned_data['image']
                if text is not None or image is not None:
                    is_send_visible = True
                else:
                    is_send_visible = False
                if image is not None:
                    pilImage = Image.open(image)
                    
                    if pilImage.mode != 'RGB':
                        pilImage = pilImage.convert('RGB')

                    pilImage = convert_to_jpeg(pilImage)

                    resized_image = pilImage.resize((int(pilImage.width * 0.5), int(pilImage.height * 0.5)))  

                    encodedImage = profile_of_receiver.rb.encrypt_image(resized_image, profile_of_receiver.rb.n_var)
                else:
                    encodedImage = None

                message = Message.objects.create(sender=request.user, receiver=receiver, text=text, image=encodedImage)
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
        lst = []
        for m in messages:
            if m.message.sender == request.user:
                decoded = profile_of_receiver.rb.decode(json.loads(m.message.text))
            else:
                decoded = profile_of_sender.rb.decode(json.loads(m.message.text))
            if m.message.image:
                decoded_image = profile_of_sender.rb.decode_image(json.loads(m.message.image))
                lst.append((decoded, m.message.sender, m.date, image_to_base64(decoded_image)))
            else:
                lst.append((decoded, m.message.sender, m.date, None))
        context = {'form': form, 'messages': lst, 'receiver': receiver, 'profile_of_receiver': profile_of_receiver, "is_send_visible": is_send_visible}
        return render(request, 'message_app/message.html', context)
    else:
        messages = MessageHistory.objects.filter(user=request.user).order_by('-date')
        context = {'messages': messages}
        return render(request, 'message_app/message_history.html', context)

def convert_to_jpeg(pil_image):
    # Create an in-memory buffer
    image_buffer = BytesIO()

    # Save the image to the buffer as JPEG
    pil_image.save(image_buffer, format='JPEG', quality=10)

    # Seek to the beginning of the buffer
    image_buffer.seek(0)

    # Open the JPEG image from the buffer
    jpeg_image = Image.open(image_buffer)

    # Return the PIL Image in JPEG format
    return jpeg_image


def image_to_base64(pil_image):
    from io import BytesIO

    # Create a BytesIO object to hold the image data
    image_buffer = BytesIO()
    
    pil_image = pil_image.convert('RGB')
    # Save the PIL image to the BytesIO buffer in JPEG format
    pil_image.save(image_buffer, format='JPEG')
    
    # Get the base64-encoded image data from the buffer
    base64_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')

    return base64_data

@login_required
def chat_history(request, pk=None):
    """
    This method show user's chat history.
    """
    if request.method == 'POST':
        if 'search' in request.POST:
            return redirect(message, pk=request.POST['name'])
        for user in User.objects.all():
            if user.username in request.POST:
                return redirect(f"/message/{user.username}/")
    user = get_object_or_404(User, username=pk)
    set_with_results = set()
    for i in MessageHistory.objects.filter(user=user.id):
        if str(i.message.receiver) != request.user.username:
            set_with_results.add(i.message.receiver)
    return render(request, 'message_app/message_history.html', {'user':set_with_results, "username": pk})
