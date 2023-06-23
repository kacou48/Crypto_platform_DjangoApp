from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser 
from .managers import UserManager
from .utils import generate_ref_code
  

#Create user model
class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    accepter = models.BooleanField(default=False, blank=False, null=False)
    
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


"""
cette classe es liee a signals et init et apps
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommende_par = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    mes_recommendations = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"

    def get_recommended_profile(self):
        qs = Profile.objects.all()
        #my_recs = [p for p in qs if p.recommende_par == self.user]
        my_recs = []
        for profile in qs:
            if profile.recommende_par == self.user:
                my_recs.append(profile)

        return my_recs
    

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)





class InfoDeTransaction(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cle_id = models.CharField(max_length=200)
    date_de_creation = models.DateTimeField(default=timezone.now)
    paying_address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.cle_id)