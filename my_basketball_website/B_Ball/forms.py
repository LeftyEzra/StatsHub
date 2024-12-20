from django import forms
from .models import Team, Organizer, Player, Competition, GameSchedule, Standing
from django.forms import inlineformset_factory






"""



class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'

class GameScheduleForm(forms.ModelForm):
    class Meta:
        model = GameSchedule
        fields = '__all__'

class StandingForm(forms.ModelForm):
    class Meta:
        model = Standing
        fields = '__all__'

"""



class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = '__all__'

        labels = {
            'name': 'Name',
            'contact_info': 'Contacts',
            'competitions': 'Competition Name',
            'organizer_logo': 'Upload Logo or Picture',

        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Information'}),
            'competitions': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Select Competitions'}),
            'organizer_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# COMPETITION FORM

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'
        labels = {
            'organizers': 'Host Name',
            'name': 'Competition Name',
            'start_date': 'Starting Date',
            'end_date': 'End Date',
            'teams': 'Participating Teams',
            'location': 'Location',
            'year': 'Year',
            'description': 'Description',
        }
        widgets = {
            'organizers': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Competition Name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'teams': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Brief description about this competition.'}),
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'team_name', 'team_logo', 'team_abbreviation',
            'team_head_coach', 'head_coach_photo',
            'team_assitance_coach1', 'assitance_coach1_photo',
            'team_assitance_coach2', 'assitance_coach2_photo'
        ]

        labels = {
            'team_name': 'Enter Team Name',
            'team_logo': 'Team Logo',
            'team_abbreviation': 'Team Abbreviation',
            'team_head_coach': 'Team Head Coach',
            'head_coach_photo': 'Head Coach Photo',
            'team_assitance_coach1': 'Assistant Coach 1',
            'assitance_coach1_photo': 'Assistant Coach 1 Photo',
            'team_assitance_coach2': 'Assistant Coach 2',
            'assitance_coach2_photo': 'Assistant Coach 2 Photo',
        }

        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'team_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'team_abbreviation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Abbreviation'}),
            'team_head_coach': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Team Head Coach's Name"}),
            'head_coach_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'team_assitance_coach1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assistant Coach Name'}),
            'assitance_coach1_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'team_assitance_coach2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assistant Coach Name'}),
            'assitance_coach2_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

        labels = {
            'jersey_numbers': 'Jersey Number',
            'player_name': 'Player Name',
            'player_age': 'Age',
            'position': 'Position',
            'height': 'Height',
            'weight': 'Weight',
            'player_image': "Player's Image",
            'player_club': 'Current Club',
            'team_name': 'Nationality',
        }

        widgets = {
            'jersey_numbers': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jersey Number'}),
            'player_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Player's Name"}),
            'player_age': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Position"}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Height"}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Weight'}),
            'player_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'player_club': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Club'}),
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nationality"}),
        }

# Inline formset for players
PlayerFormSet = inlineformset_factory(Team, Player, form=PlayerForm, extra=1)
