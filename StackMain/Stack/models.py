from django.db import models

# Create your models here.

class user(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=40, primary_key=True)
    password = models.CharField(max_length=32)
    # records if user is active for security purposes
    active = models.BooleanField
    forget_password_token = models.CharField(max_length=100, default="")

class task(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    lock = models.BooleanField()
    recurring = models.BooleanField()
    time = models.TimeField()