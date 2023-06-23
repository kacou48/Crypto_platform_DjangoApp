from django.contrib import admin
from .models import User, InfoDeTransaction, Profile


admin.site.register(User)
admin.site.register(InfoDeTransaction)
admin.site.register(Profile)

