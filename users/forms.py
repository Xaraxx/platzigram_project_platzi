
from django import forms
from django.contrib.auth.models import User

from users.models import Profile

class ProfileForms(forms.Form):
    
    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    picture = forms.ImageField()

class SignupForms(forms.Form):

    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(max_length=50,
    widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=50,
    widget=forms.PasswordInput())
    
    first_name = forms.CharField(min_length=4, max_length=20)
    last_name = forms.CharField(min_length=4, max_length=20)
    email = forms.CharField(widget=forms.EmailInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()

        if username_taken:
            raise forms.ValidationError('Username is already in use')
        return username

    def clean(self):
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')
        
        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()





