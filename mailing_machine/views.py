from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import WoBoConnection
from .forms import CreateWoBoConnection
from .functions import build_data_sheet

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
