from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError

from .models import *
from .forms import *
from .functions import *

from datetime import datetime
import os


# Create your views here.
def index(request):
    template = 'pages/index.html'
    
    return render(request=request, context={'': ''}, template_name=template)


@login_required()
def create_new_export(request):
    
    template = 'pages/create_wobo_output.html'
    context = dict()
    
    form = CreateWoBoCompany()
    context['companies'] = WoBoCompany.objects.all()
    context['exports'] = WoBoConnection.objects.filter(user=request.user)
    api_key = request.GET.get('api_key')
    
    if api_key:
        
        try:
            context['company'] = WoBoConnection.objects.get(company__api_key=api_key)
            context['company'].file = build_data_sheet(api_key=api_key)
            context['company'].file_update_date = datetime.now()
            context['company'].save()
            
        except WoBoConnection.DoesNotExist:
            wobo_connect = {
                'company': WoBoCompany.objects.get(api_key=api_key),
                'user': request.user,
                'date_created': datetime.now(),
                'file_update_date': datetime.now(),
                'file': build_data_sheet(api_key=api_key)
            }
    
            WoBoConnection.objects.get_or_create(**wobo_connect)
        except IntegrityError or AttributeError or TypeError:
            messages.error(request=request, message=_('Invalid API Key or non-existent key.'))

    if request.method == 'POST':
        form = CreateWoBoCompany(request.POST)
        
        if form.is_valid():
            form = form.save(commit=True)
            wobo_connect = {
                'company': form,
                'user': request.user,
                'date_created': datetime.now(),
                'file_update_date': datetime.now(),
                'file': build_data_sheet(api_key=form.api_key)
            }
            
            WoBoConnection.objects.get_or_create(**wobo_connect)
            
            form.save()
            
        else:
            messages.error(request=request, message=_('The form is invalid...'))

    context['form'] = form
    context['exports'] = WoBoConnection.objects.filter(user=request.user, company__api_key=api_key).order_by(
        '-date_created')
    
    return render(request=request, context=context, template_name=template)


def schedule_sessions(request):
    
    context = dict()
    api_key = None
    form = CreateWoBoCompany()
    context['form'] = form
    
    if request.method == 'POST':
        context['company'] = WoBoCompany.objects.get_or_create(api_key=api_key, company_name=request.POST.get('company_name'))
        api_key = request.POST.get('api_key')
        
    else:
        api_key = request.GET.get('api_key')
        try:
            context['company'] = WoBoCompany.objects.get(api_key=api_key)
        except WoBoCompany.DoesNotExist:
            pass
        
    if 'company' in context.keys():
        context['teams'] = get_teams(api_key=api_key)
        context['users'] = get_users(api_key=api_key)

    template = 'pages/schedule_sessions/overview.html'
    context['form'] = form
    context['companies'] = WoBoCompany.objects.all()
    context['org_chart'] = build_org_chart(api_key=api_key)
    
    return render(request=request, context=context, template_name=template)