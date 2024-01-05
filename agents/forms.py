""" 
FORMS.PY
this will hold any forms related spceially to this app [agents], its getting models from other apps in the project to fullfill ista operatins like Agnet class from leads module
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User=get_user_model()

class AgentModelForm(forms.ModelForm):
    """ ModelForm for agent"""
    
    class Meta:
        model=User
        fields=(
            'email',
            'username',
            'first_name',
            'last_name'
        )
