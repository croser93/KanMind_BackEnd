from django.db import models

class UserRegestration(models.Model):
    fullname = models.CharField(max_length= 120)
    email = models.CharField(max_length= 120)
    password = models.CharField(max_length=255)
    
