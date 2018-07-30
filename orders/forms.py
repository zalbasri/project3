# basis for code: https://www.youtube.com/watch?v=66l9b2QrBR8
# https://docs.djangoproject.com/en/2.0/topics/forms/

from django import forms # for creating forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# inhereting from django the UserCreationForm which has a username
# feild, password1, password2
class RegisterationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)


    # information about the user created
    class Meta:
        model = User

        # fields in the User model imported and feilds added
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
            )

    # adds the data to models and the databade
    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)

        # cleaned_data so user can't hack into website with code
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # adds user to database
        if commit:
            user.save()

        return user