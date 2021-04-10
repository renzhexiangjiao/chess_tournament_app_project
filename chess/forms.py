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

class ChooseTournamentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = None
        if 'user' in kwargs:
            user = kwargs.pop('user')
        super(ChooseTournamentsForm, self).__init__(*args, **kwargs)

        label = "Choose one tournament or more:"

        if user:
            tournament_choices = zip(Tournament.objects.exclude(participants=user).order_by('id').values_list('id', flat=True), 
                                     Tournament.objects.exclude(participants=user).order_by('id').values_list('name', flat=True))
        else:
            tournament_choices = zip(Tournament.objects.all().order_by('id').values_list('id', flat=True), 
                                     Tournament.objects.all().order_by('id').values_list('name', flat=True))

        self.fields['tournaments'] = forms.MultipleChoiceField(choices=tournament_choices,
                                                               label=label,
                                                               widget=forms.CheckboxSelectMultiple(),
                                                               required=False)
    
    

