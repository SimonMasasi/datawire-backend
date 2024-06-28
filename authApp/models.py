from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.db import models
import string
from random import choices

class CustomUser(AbstractUser):
    age = models.IntegerField(default=4)
    email = models.EmailField(max_length=50, unique=True)
    verification_code = models.CharField(max_length=6, default=0)
    roles = models.ManyToManyField('Role', through='UserRole')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def generate_verification_code(self):
        characters = string.ascii_letters + string.digits
        code = ''.join(choices(characters, k=6))
        self.verification_code = code
        self.save()

    def __str__(self):
        return self.username
    
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.TextField()  # Define permissions for each role

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


