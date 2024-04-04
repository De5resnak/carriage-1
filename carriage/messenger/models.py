from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class GroupChat(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(GroupChat, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.sender.username} to {self.chat.name}: {self.text}"
