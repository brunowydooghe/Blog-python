from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#
#from django.forms.widgets import ChoiceWidget
#from django.views.generic import CreateView

from blog.models import Post





choice_list = forms.ChoiceField(choices='', required=False, widget=forms.Select(attrs={'data-toggle': 'select'}))


# choices = [('programming lanuages', 'programming lanuages'), ('design', 'design')]
# choices = Category.objects.all().value_list('name', 'name')
# choice_list = []

# for item in choices:
#    choice_list.append(item)
# def should_be_empty(value):
#    if value:
#        raise forms.ValidationError('Field is not empty')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label="Leave empty")


# Override the UserCreationForm
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This already exists!'})
    #first_name = forms.CharField(max_length=100)
    #last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class PostForm(forms.ModelForm):
    model = Post
    fields = ('title', 'author', 'category', 'keywords', 'image')

    def __init__(self, user, is_authenticated, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        choice_list = []
        for choices in Post.objects.filter(role=1):
            choice_list.append(choices.name)
        self.fields['category'].choices = [(None, '--------')] + choice_list

    widgets = dict(title=forms.TextInput(attrs={'class': 'form-control'}),
                   author=forms.Select(attrs={'class': 'form-control'}),
                   category=forms.Select(choices='', attrs={'class': 'form-control'}),
                   keywords=forms.Textarea(attrs={'class': 'form-control'}))

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'keywords')
        widgets = dict(title=forms.TextInput(attrs={'class': 'form-control'}),
                       author=forms.Select(attrs={'class': 'form-control'}),
                       category=forms.Select(choices='', attrs={'class': 'form-control'}),
                       keywords=forms.Textarea(attrs={'class': 'form-control'}))
