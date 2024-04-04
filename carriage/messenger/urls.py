from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth.views import LoginView, LogoutView

router = DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groupchats', views.GroupChatViewSet)

urlpatterns = [
    path('', views.index, name='default'),
    path('api/chat/<int:chat_id>/', views.chat_detail_view, name='chat_detail'),


    path('api/chats/', views.ChatListView.as_view(), name='chat-list'),
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('api/chat/<int:chat_id>/send-message/', views.send_message, name='send_message'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('create-chat/', views.create_chat_view, name='create_chat'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
]
