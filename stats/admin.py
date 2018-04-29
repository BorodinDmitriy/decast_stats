# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import AuthReport, PayBillReport, ChangeAccountReport

# Register your models here.
admin.site.register(AuthReport)
admin.site.register(PayBillReport)
admin.site.register(ChangeAccountReport)
