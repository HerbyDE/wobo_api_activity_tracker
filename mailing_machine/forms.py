from django.forms import ModelForm

from .models import *
        
        
class CreateWoBoCompany(ModelForm):
    
    class Meta:
        model = WoBoCompany
        fields = ['company_name', 'api_key']