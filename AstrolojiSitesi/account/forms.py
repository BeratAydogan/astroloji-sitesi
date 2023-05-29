from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from astrolojisitem.models import Profile, Post


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    gun = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                             validators=[MinValueValidator(1), MaxValueValidator(31)])
    ay = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                            validators=[MinValueValidator(1), MaxValueValidator(12)])
    yil = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                             validators=[MinValueValidator(1900), MaxValueValidator(2023)])
    gonder = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                label='Receive updates', required=False)

    class Meta:
        model = Profile
        fields = ['gun', 'ay', 'yil', 'gonder']


class NewPostForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Enter your post'}
        ),
        max_length=4000,
        help_text='Max length is 4000 characters.'
    )

    class Meta:
        model = Post
        fields = ['message']