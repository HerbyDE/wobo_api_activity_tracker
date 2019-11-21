from django.urls import re_path, include

from mailing_machine.views import index

urlpatterns = [
    re_path('^$', index, 'index')
]