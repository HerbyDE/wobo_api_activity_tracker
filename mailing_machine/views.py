from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    template = 'pages/index.html'
    
    return render(request=request, context={'': ''}, template_name=template)
