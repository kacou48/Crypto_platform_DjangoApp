from django.shortcuts import render
import json
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponse
from accounts.models import Profile

def index_view(request, *args, **kwargs):
    try:
        url_list_current = "https://api.changenow.io/v1/currencies?active=true&fixedRate=true"
        data_list_current = requests.get(url_list_current).json()
    
    except:
        data_list_current = {}    
    """
    les lignes suplementaires correspondent au lien
    de reference qui redirige sur page d'accuiel 
    """
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        #print('id',profile.id)
    except:
        pass
    
    context = {
        'data_list_current': data_list_current,
    }
    return render(request, 'core/index.html', context)


class PolicyView(TemplateView):
    template_name = 'core/policy.html'