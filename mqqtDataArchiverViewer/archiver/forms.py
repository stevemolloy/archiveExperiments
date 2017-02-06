from django import forms
from .models import registry

class UnknownForm(forms.Form):
    active1 = forms.BooleanField(label = 'Signal 1', required=False, initial=True)
    active2 = forms.BooleanField(label = 'Signal 2', required=False, initial=True)

class ActiveSignalForm(forms.Form):
    regObjs = registry.objects.order_by('first_registered')
    selection = ((sig.id, sig.signal) for sig in regObjs)
    choices = forms.MultipleChoiceField(
        label = 'Alter Archiver Registry',
        choices = selection,
        widget = forms.CheckboxSelectMultiple,
        initial = [sig.id for sig in regObjs if sig.archival_active],
    )
