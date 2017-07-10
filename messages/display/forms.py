from django import forms

scoreboard_choices = (
    ('job_state_scbd', 'Job State SCBD'),
    ('ack_scbd', 'Ack SCBD')
)

class table_time_query(forms.Form):
    choose_scoreboard = forms.MultipleChoiceField(choices=scoreboard_choices, widget=forms.CheckboxSelectMultiple())
    start_time = forms.CharField(label='Start time')
    end_time = forms.CharField(label='End time')

