from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.


class WoBoConnection(models.Model):
    company = models.CharField(verbose_name=_('Company Name'), max_length=75)
    admin_key = models.CharField(verbose_name='WoBo API Key for admin account', max_length=125)
    user = models.ForeignKey(verbose_name=_('Creator'), to='auth.User', on_delete=models.SET_NULL, null=True)
    file = models.FileField(verbose_name=_('Latest Export File'), upload_to='wobo_export_files')
    date_created = models.DateTimeField(auto_now=True)
    file_update_date = models.DateTimeField(auto_now=True)
    
    
