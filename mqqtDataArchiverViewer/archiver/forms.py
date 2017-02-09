from django import forms
from .models import registry

class ActiveSignalForm(forms.Form):
    choices = forms.MultipleChoiceField(
        label = 'Alter Archiver Registry',
        choices = lambda: ((sig.id, sig.signal)
            for sig in registry.objects.order_by('first_registered')),
        widget = forms.CheckboxSelectMultiple,
        initial = lambda: [
            sig.id for sig in registry.objects.order_by('first_registered')
            if sig.archival_active],
    )
