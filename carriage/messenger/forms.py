from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, GroupChat

class ProfileEditForm(forms.ModelForm):
    new_username = forms.CharField(max_length=150, required=False, label='Новый никнейм')

    class Meta:
        model = UserProfile
        fields = ['avatar', 'status', 'new_username']

class ChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name', 'members']

class CustomSignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    status = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'avatar', 'status')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = UserProfile.objects.create(user=user, avatar=self.cleaned_data['avatar'], status=self.cleaned_data['status'])
        return user