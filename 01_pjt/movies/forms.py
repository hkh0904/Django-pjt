from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    
    score = forms.FloatField(
        widget= forms.NumberInput(
            attrs= {'step': 0.5, 
                    'max': 5, 
                    'min': 0}
            )
        )                                        

    release_date = forms.DateField(
        widget= forms.DateInput(
            attrs= {'type': 'date'}
            )
    )
    
    class Meta:
        model = Movie
        fields = '__all__'