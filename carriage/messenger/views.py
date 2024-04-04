from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Message, User, GroupChat, UserProfile
from .serializers import MessageSerializer, UserSerializer, GroupChatSerializer
from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from .forms import ProfileEditForm, ChatForm, CustomSignUpForm
from django.contrib.auth.decorators import login_required

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer

@login_required
def index(request):
    current_user = request.user
    user_group_chats = GroupChat.objects.filter(members=current_user)
    context = {'user_group_chats': user_group_chats}
    return render(request, 'default.html', context)


@csrf_exempt
def send_message(request, chat_id):
    if request.method == 'POST':
        logger.info(f'Received POST request to send message for chat ID {chat_id}')
        try:
            data = json.loads(request.body)
            message_text = data.get('text', '')
        except json.JSONDecodeError:
            logger.error('Invalid JSON data in the request body')
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if not message_text:
            logger.error('Message text is empty')
            return JsonResponse({'error': 'Message text cannot be empty'}, status=400)

        chat = get_object_or_404(GroupChat, pk=chat_id)
        message = Message.objects.create(text=message_text, sender=request.user, chat=chat)
        logger.info(f'Message created with ID {message.id}')
        return JsonResponse({'success': True, 'message_id': message.id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def chat_detail_view(request, chat_id):
    chat = get_object_or_404(GroupChat, pk=chat_id)
    serializer = GroupChatSerializer(chat)
    return JsonResponse(serializer.data)

class ChatListView(APIView):
    def get(self, request):
        chats = GroupChat.objects.filter(members=request.user)
        data = [{'id': chat.id, 'name': chat.name} for chat in chats]
        return Response(data)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [{'id': user.id, 'name': user.username} for user in users]
        return Response(data)

class GroupChatList(APIView):
    def get(self, request):
        chat_list = GroupChat.objects.all()
        serializer = GroupChatSerializer(chat_list, many=True)
        return Response(serializer.data)

@login_required
def profile_edit(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        initial_data = {'avatar': user_profile.avatar, 'status': user_profile.status, 'new_username': request.user.username}
        form = ProfileEditForm(instance=user_profile, initial=initial_data)
    return render(request, 'profile_edit.html', {'form': form})

def create_chat_view(request):

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()
            form.save_m2m()
            logger.info(f'Received POST request to send message for chat ID')
            return redirect('/')
    else:
        form = ChatForm()
        users = User.objects.all()
    return render(request, 'create_chat.html', {'form': form, 'users': User.objects.all()})

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})