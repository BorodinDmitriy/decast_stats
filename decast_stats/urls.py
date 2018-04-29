"""decast_stats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin

from stats import views as stats_views

from rest_framework.urlpatterns import format_suffix_patterns


# removable block
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token

authorization_urls = [
  url(r'^api-token-auth/', obtain_jwt_token),
  url(r'^api-token-refresh/', refresh_jwt_token),
  url(r'^api-token-verify/', verify_jwt_token),
  ]
# removable block end


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',stats_views.index, name="index"),
    url(r'^dashboard/$',stats_views.dashboard, name="dashboard"),
    url(r'^auth/',include(authorization_urls)),
    url(r'^auth_report/$',stats_views.auth_report, name="auth_report"),
    url(r'^pay_bill_report/$',stats_views.pay_bill_report, name="pay_bill_report"),
    url(r'^change_account_report/$',stats_views.change_account_report, name="change_account_report"),
]
