from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError

from .models import *
from .forms import *
from .functions import *

import datetime
import os


# Create your views here.
def index(request):
    template = 'pages/index.html'
    
    return render(request=request, context={'': ''}, template_name=template)


@login_required()
def create_new_export(request):
    
    template = 'pages/create_wobo_output.html'
    context = dict()
    
    form = CreateWoBoConnection()
    
    if request.method == 'POST':
        form = CreateWoBoConnection(request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.date_created = datetime.datetime.now()
            form.file_update_date = datetime.datetime.now()
            
            form.file = build_data_sheet(api_key=form.admin_key)
            
            form.save()
            
        else:
            messages.error(request=request, message=_('The form is invalid...'))

    context['form'] = form
    context['exports'] = WoBoConnection.objects.filter(user=request.user)

    return render(request=request, context=context, template_name=template)


def schedule_sessions(request):
    
    context = dict()
    
    api_key = request.GET.get('api_key')
    
    if api_key:
        company = WoBoCompany.objects.get_or_create(api_key=api_key)
        context['company'] = company
        context['users'] = get_users(api_key=api_key)['data']['user']
        context['teams'] = WoBoTeam.objects.filter(company__api_key=api_key)
        template = 'pages/schedule_sessions/overview.html'
        
    else:
        template = 'pages/schedule_sessions/overview.html'
        
    form = CreateWoBoCompany()
    
    if request.method == 'POST':
        form = CreateWoBoCompany(request.POST)
        post_api_key = request.POST.get('api_key')
        context['users'] = get_users(api_key=post_api_key)['data']['user']
        
        try:
            context['company'] = WoBoCompany.objects.get(api_key=post_api_key)
            messages.success(request=request, message=_('Company results fetched successfully.'))
        except WoBoCompany.DoesNotExist:
            if form.is_valid():
                form = form.save(commit=False)
                form.save()
                context['company'] = form
                messages.success(request=request, message=_('Company created successfully.'))
            else:
    
                messages.error(request=request, message=_('Invalid API Key. Please try again.'))

        if context['company'] and context['users']:
            data = get_teams(post_api_key)['data']['team']
            output = list()
            
            for team in data:
                        
                t = {
                    'id': int(team['team_id']),
                    'name': team['team_name'],
                    'manager': int(team['team_owner']),
                    'company': context['company']
                }
                
                try:
                    t['parent_team'] = WoBoTeam.objects.get_or_create(pk=int(team['parent_team_id']))[0]
                except TypeError:
                    pass
                except ValueError:
                    pass
                
                try:
                    team_inst = WoBoTeam.objects.get(pk=team['team_id'])
                
                    team_inst.name = team['team_name']
                    team_inst.manager = int(team['team_owner'])
                    team_inst.company = context['company']
                    team_inst.save()
                    output.append(team_inst)
                    
                except AttributeError:
                    pass
                    
                except WoBoTeam.DoesNotExist:
                    team_inst = WoBoTeam.objects.create(**t)
                    output.append(team_inst)

                for user in context['users']:
                    u = {
                        'id': user['user_id'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'email': user['email'],
        
                    }
                    us = WoBoTeamMember.objects.get_or_create(**u)[0]
                    
                    try:
                        us.teams.add(int(user['team_id']))
                        us.save()
                    except IntegrityError:
                        pass
                    
            context['teams'] = output
            
        else:
            pass
    
        return HttpResponseRedirect('/schedule/?api_key={}'.format(post_api_key))
     
    context['form'] = form
        
    return render(request=request, context=context, template_name=template)