from django.contrib.auth.forms import UserCreationForm
from .models import WORKitUser, Profile



class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WORKitUser
        fields = ("first_name", "last_name", "email", "username", "password1", "password2", "gender")

    
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            userprofile = Profile()
            userprofile.user = user
            userprofile.save()
        return user
