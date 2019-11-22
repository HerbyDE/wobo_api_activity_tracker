from django.forms import ModelForm

from .models import *


class CreateWoBoConnection(ModelForm):
    
    class Meta:
        model = WoBoConnection
        fields = ['company', 'admin_key']
        
        
class CreateWoBoCompany(ModelForm):
    
    class Meta:
        model = WoBoCompany
        fields = ['company_name', 'api_key']