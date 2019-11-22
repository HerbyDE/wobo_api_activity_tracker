from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.


class WoBoConnection(models.Model):
    company = models.CharField(verbose_name=_('Company Name'), max_length=75)
    admin_key = models.CharField(verbose_name='WoBo API Key for admin account', max_length=125)
    user = models.ForeignKey(verbose_name=_('Creator'), to='auth.User', on_delete=models.SET_NULL, null=True)
    file = models.FilePathField(verbose_name=_('Latest Export File'))
    date_created = models.DateTimeField(auto_now=True)
    file_update_date = models.DateTimeField(auto_now=True)
    
    
class WoBoCompany(models.Model):
    api_key = models.CharField(verbose_name=_('API Key'), max_length=75, primary_key=True)
    company_name = models.CharField(verbose_name=_('Company Name'), max_length=125, null=True, blank=True)
    
    def __str__(self):
        return '{}'.format(self.company_name)
    
    
class WoBoTeam(models.Model):
    id = models.AutoField(verbose_name=_('WoBo Team ID'), primary_key=True)
    name = models.CharField(verbose_name=_('Team Name'), max_length=125)
    company = models.ForeignKey(verbose_name=_('Company'), to=WoBoCompany, on_delete=models.CASCADE, null=True)
    parent_team = models.ForeignKey(verbose_name=_('Parent Team'), to='mailing_machine.WoBoTeam',
                                    on_delete=models.CASCADE, blank=True, null=True)
    manager = models.IntegerField(verbose_name=_('Team Manager'), null=True)
    sessionDate = models.DateField(verbose_name=_('Session Date'), null=True)
    preMailSent = models.BooleanField(verbose_name=_('Pre-session E-Mail sent'), default=False)
    postMailSent = models.BooleanField(verbose_name=_('Post-session E-Mail sent'), default=False)
    
    def __str__(self):
        
        try:
            cn = self.company.company_name
        except AttributeError:
            cn = 'ERROR'
        
        return '{} - {}'.format(self.name, cn)
    
    
class WoBoTeamMember(models.Model):
    first_name = models.CharField(verbose_name=_('First Name'), max_length=125)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=125)
    email = models.EmailField(verbose_name=_('E-Mail'))
    teams = models.ManyToManyField(verbose_name=_('Teams'), to=WoBoTeam, related_name='teams')
    
    def __str__(self):
        return '{} {} - {}'.format(self.first_name, self.last_name, self.email)
