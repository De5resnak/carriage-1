from rest_framework import serializers
from .models import Message, User, GroupChat

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Позволяет включить сообщения для каждого чата

    class Meta:
        model = GroupChat
        fields = '__all__'