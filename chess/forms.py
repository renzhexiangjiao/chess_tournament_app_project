from django import forms
from chess.models import AccountPage, Tournament
from django.contrib.auth.models import User
from django.utils import timezone

class AccountPageForm(forms.ModelForm):
    status = forms.CharField(max_length=100, help_text="Please enter the status.")
    class Meta:
        model = AccountPage
        fields = ('status', 'picture',)
        
class TournamentForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Please enter the tournament name.")
    date = forms.SplitDateTimeField(label='Pick date and time:', initial=timezone.now(), widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type':'time'}, time_format='%H:%M'))
    class Meta:
        model = Tournament
        fields = ('name', 'date',)