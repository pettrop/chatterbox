from logging import getLogger

from django.core.exceptions import ValidationError
from django.forms import Form, Textarea, ModelForm
from django import forms

from base.models import Room
LOGGER = getLogger()

class RoomForm(ModelForm):
    # name = forms.CharField(max_length=200)
    # description = forms.CharField(widget=Textarea, required=False)

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants']


    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            validation_error = "Name must contains min. 2 chars."
            LOGGER.warning(f'{validation_error} : {name}')
            raise ValidationError(validation_error)
        return name