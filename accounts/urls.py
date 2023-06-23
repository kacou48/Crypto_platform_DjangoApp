from django.urls import path
from django.contrib.auth import views as auth_views
from .views import seconnecter, UserRegistrationView, LogoutView, activate_user, BlogView, LoginPageView, keepInfo, monCompte


app_name = 'accounts'

urlpatterns = [
    path(
        "login/", LoginPageView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),

    path(
        "activate-user/<uidb64>/<token>", activate_user, name="activate"
    ),
    path('process_connection/', seconnecter, name='process_connection'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('process_transaction/', keepInfo, name='process_transaction'),
    path('mon-compte/', monCompte, name='mon-compte'),


    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='accounts/password_reset_email.html',
             success_url='accounts/user_login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
