from django.forms import ModelForm
from django import forms
from .models import *
from django.utils.safestring import mark_safe
import uuid

# Create the form class.
class MyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class CompanyForm(MyModelForm):
    class Meta:
        model = Company
        exclude = Company.hidden_fields


