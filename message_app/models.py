# from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     friends = models.ManyToManyField('self', blank=True)

#     def __str__(self):
#         return self.user.username
    
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     text = models.TextField()
#     image = models.ImageField(upload_to='media/', blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True)

# class MessageHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_history')
#     message = models.ForeignKey(Message, on_delete=models.CASCADE)
#     read = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import User
from .rabin_cryptosystem import RabinCryptography

class UserProfile(models.Model):
    rb = RabinCryptography()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #friends = models.ManyToManyField('self', blank=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    image = models.TextField(null=True)
    image_name = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_history')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
