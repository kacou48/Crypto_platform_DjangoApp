from django.urls import path

from .views import PolicyView



app_name = 'core'

urlpatterns = [
    path('policy/', PolicyView.as_view(), name='policy'),   
]