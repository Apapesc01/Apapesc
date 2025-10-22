from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove "superuser" dos choices do user_type
        user_type_field = self.fields.get('user_type')
        if user_type_field:
            user_type_field.choices = [
                (value, label)
                for value, label in user_type_field.choices
                if value != 'superuser'
            ]