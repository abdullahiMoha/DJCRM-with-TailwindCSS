"""
Here we will create most of the forms in LEADS App     
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UsernameField
from .models import Lead,Agent

User=get_user_model()

class LeadModelForm(forms.ModelForm):
    """ 
    LeadModelForm 
    """
    class Meta:
        """ Meta Class for LeadModelForm """
        model=Lead
        fields=(
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )

class LeadForm(forms.Form):
    """ 
    LeadForm
    """
    first_name=forms.CharField()
    last_name=forms.CharField()
    age=forms.IntegerField(min_value=0)
    
class CustomUserCreationForm(UserCreationForm):
    """ 
    Our Custum for user creation form
    """
    class Meta:
        """ Meta Class for our custom user creation form"""
        model=User
        fields=("username",)
        field_classes={"username": UsernameField}

class AssignAgentForm(forms.Form):
    """ AssignAgent form"""
    # pylint: disable=no-member
    agent=forms.ModelChoiceField(queryset=Agent.objects.none())
    
    def __init__(self, *args, **kwargs):
        request=kwargs.pop("request")
        agents=Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args,**kwargs)
        self.fields["agent"].queryset=agents

class LeadCategoryUpdateForm(forms.ModelForm):
    """ModelForm for updating LeadCategory"""
    class Meta:
        """ Meta Class for LeadModelForm """
        model=Lead
        fields=(
            'category',
        )