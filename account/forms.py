# In your_app_name/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from account.models import Account, CustomUser2, Posts, Replies

from django.contrib.auth.models import User


# From video       

class CreateUserForm(UserCreationForm):
    email = forms.EmailField
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_teacher = forms.CheckboxInput()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')#, 'is_teacher')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['is_teacher']
# New
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField()

''' class Meta:
        model = PostFile 
        fields = ['file']'''


class PostForm(forms.ModelForm):
    #file_field = MultipleFileField()
    class Meta:
        model = Posts
        fields = ('title', 'author', 'body', 'snippet', 'file')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'User', 'type': 'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            
        }

class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            #'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'User', 'type': 'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class UpdatePostForm(forms.ModelForm):
    #file_field = MultipleFileField()
    class Meta:
        model = Posts
        fields = ('title', 'body', 'snippet', 'file')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


