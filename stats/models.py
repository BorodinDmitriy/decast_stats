# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AuthReport(models.Model):
  id = models.AutoField(primary_key=True)
  email = models.CharField(max_length=50)
  status = models.BooleanField()
  date = models.DateField(auto_now_add=True)
  
  
class PayBillReport(models.Model):
  id = models.AutoField(primary_key=True)
  personal_account = models.CharField(max_length=50)
  rate = models.FloatField(default=0.0)
  reading = models.CharField(max_length=50)
  status = models.BooleanField()
  date = models.DateField(auto_now_add=True)
  
class ChangeAccountReport(models.Model):
  id = models.AutoField(primary_key=True)
  old = models.CharField(max_length=50)
  new = models.CharField(max_length=50)
  status = models.BooleanField()
  date = models.DateField(auto_now_add=True)
  