from django.forms import ModelForm

from .models import WoBoConnection


class CreateWoBoConnection(ModelForm):
    
    class Meta:
        model = WoBoConnection
        fields = ['company', 'admin_key']
        