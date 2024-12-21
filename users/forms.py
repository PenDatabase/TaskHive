from django.contrib.auth.forms import UserCreationForm
from .models import WORKitUser, Profile



class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WORKitUser
        fields = ("first_name", "last_name", "email", "username", "password1", "password2", "gender")

    
    def save(self, commit = True):
        userprofile = Profile()
        userprofile.user = self.model
        return super().save(commit)
