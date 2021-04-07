from django import forms
from chess.models import AccountPage
from django.contrib.auth.models import User

class AccountPageForm(forms.ModelForm):
    status = forms.CharField(max_length=100, help_text="Please enter the status.")
    class Meta:
        model = AccountPage
        fields = ('status', 'picture',)