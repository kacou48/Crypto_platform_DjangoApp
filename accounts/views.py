from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.http import JsonResponse
import json

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader  import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading


from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, View
from django.db.models import F

from .forms import UserRegistrationForm, LoginForm
from .models import InfoDeTransaction, Profile




class EmailThread(threading.Thread):
    
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


User = get_user_model()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'ACTIVATION DE COMPTE'
    email_body = render_to_string('accounts/activation.html',{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
        })
    
    email=EmailMessage(subject=email_subject, body=email_body,
                 from_email=settings.EMAIL_HOST_USER,
                 to=[user.email]
                )
    EmailThread(email).start() # la classe qui envoie le mail.

class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'
    
    def dispatch(self, request, *args, **kwargs): # rediriger vers blog si utilisateur connecté
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('home')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        profile_id = self.request.session.get('ref_profile')
        #print('id',profile_id)
        #print(registration_form)
        

        if registration_form.is_valid():
            if profile_id is not None:

                """
                les instructions pour enregistrer celui qui recommende
                self.request.session.get('ref_profile') recupere le code du recommendé
                """
                recommended_by_profile = Profile.objects.get(id=profile_id)

                instance = registration_form.save()
                registered_user = User.objects.get(id=instance.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommende_par = recommended_by_profile.user
                registered_profile.save()
            

            user = registration_form.save()

            send_activation_email(user, request)

            
            #login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Nous vous envoyons un e-mail pour verifier votre compte.'
                    
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_login')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        
        return super().get_context_data(**kwargs)



class LoginPageView(View):
    template_name = 'accounts/user_login.html'
    form = LoginForm

    def get(self, request):
        form = self.form()
        #messages = ''
        return render(request, self.template_name,
                      context={'form':form}

        )

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password']   #verifie l'autentification...
            )

            
            if user is not None:
                if not user.is_email_verified:
                    messages.error(
                        self.request,
                        (
                            f"Cet Email n'est pas verifié, s'il vous plait consultez votre boite email."
                            
                        )
                    )
                    
                    return render(request, self.template_name, context={'form':form})

                login(request, user)
                return redirect('core:exchange-crypto')
      
        messages.error(
                    self.request,
                    (
                        f"L'addresse mail ou le password est invalide."
                        
                    )
                )
        return render(request, self.template_name, context={'form':form})







class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)



def activate_user(request, uidb64, token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user=None

    if user and generate_token.check_token(user, token):
        user.is_email_verified=True
        user.save()
        messages.success(request, "Email verifié, vous pouvez vous connectez")
        return redirect(reverse_lazy('accounts:user_login'))

    return render(request, 'accounts/activate-failed.html', {'user': user})



class BlogView(TemplateView):
    template_name = 'accounts/blog.html'


def monCompte(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    profile.mes_recommendations = len(profile.get_recommended_profile())
    profile.save()

    my_recs = len(profile.get_recommended_profile())
    
    url = "https://chiracrypto.com/" + profile.code +"/"
    #print('id',profile.code)
    print('eee',profile.mes_recommendations)
    print('my_recs', my_recs)
    try:

        info = InfoDeTransaction.objects.filter(user=user).order_by('-date_de_creation')[0]
    except:
        info = ''

    context = {'info':info, 'my_recs':my_recs, 'url': url}
    return render(request, 'accounts/compte.html', context)


#from django.views.decorators.csrf import csrf_exempt #pour le token sur navigateur privé

#@csrf_exempt
def keepInfo(request):
    print('Data: ', request.body)
    print(request.user)
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        user = request.user 
        InfoDeTransaction.objects.create(
            user = user,
            cle_id = data['form']['id'],
            paying_address = data['form']['payinAddress'],

        )
    
    return JsonResponse("Allez dans votre compte pour plus d'info", safe=False)




def seconnecter(request):
    #print('Data: ', request.body)
    data = json.loads(request.body)
    #print('data', data)
    jsonresponse = ''
    user = authenticate(email=data['form']['email'],
                password=data['form']['password']   #verifie l'autentification...
    )
    if user is not None:
        if not user.is_email_verified:
            jsonresponse += "Cet Email n'est pas verifié, s'il vous plait consultez votre boite email."
            
        else:    
            login(request, user)
    if user is  None:
        jsonresponse += "L'addresse mail ou le password est invalide."
        
    return JsonResponse(jsonresponse, safe=False)