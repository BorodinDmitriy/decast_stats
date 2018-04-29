# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from django.http import HttpResponse
from django.template import loader
from .models import AuthReport, PayBillReport, ChangeAccountReport
from validate_email import validate_email
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from tasks import *

import requests, json, pika
# Create your views here.

def check_email(email):
    return validate_email(email)
  
def check_status(status):
  if (str(status) == 'True') or (str(status) == 'False'):
    return 1
  else:
    return 0
  
def check_personal_account(personal_account):
    check_array = personal_account.split('-')
    print(check_array)
    length = len(check_array)
    if (length != 4):
      return 0
    else:
      for i in range(0,length):
	if (long(check_array[i]) == 0):
	  return 0
    return 1
  
def check_serial_number(serial_number):
    return long(serial_number)
  
def index(request):
  TestConsumer.delay()
  try:
    if request.method == 'GET':
      template = loader.get_template('index/index.html')
      context = {}
      return HttpResponse(template.render(context, request))
  
    if request.method == 'POST':
      email = request.POST["email"]
      password = request.POST["password"]
  
      is_valid_email = check_email(email)
      if (is_valid_email == 0) and (email != 'admin'):
	return redirect('index')
    
      #url = "http://localhost:8004/auth/api-token-auth/"
      url = "https://decast-stats.herokuapp.com/auth/api-token-auth/"
      headers = {'Content-Type' : 'application/json'}
      data = {'username': email, 'password': password}
      response = (requests.post(url, data=data)).json()
      print(response)
      settings.TOKEN = response["token"]
      print(settings.TOKEN)
    
      #url = "http://localhost:8004/dashboard/"
      #headers = {'Authorization': 'JWT ' + str(settings.TOKEN)}
      #response = (requests.get(url))
    
      response = redirect('dashboard')
      response['Authorization'] = "JWT " + settings.TOKEN
    
      #return render_to_response(request,'dashboard/dashboard.html', { 'token' : settings.TOKEN})
      return response
  except:
      return redirect('index')
  
  
def get_auth_count(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        print(json)
        return int(json['count'])
    except KeyError:
        return 0
@csrf_exempt
def dashboard(request):
  print(request.user)
  if (request.user.is_authenticated) and (request.user.is_superuser):
    
    # auth_reports
    auth_reports = AuthReport.objects.all()
    successful_auth_count = AuthReport.objects.filter(status=True).count()
    unsuccessful_auth_count = AuthReport.objects.filter(status=False).count()
    auth_count = auth_reports.count()
    
    users_stats = [];
    users = []
    count = 0
    for auth_report in auth_reports:
      if (not auth_report.email in users):
	users.append(auth_report.email)
	obj = {}
	obj['email'] = auth_report.email
	obj['count'] = 0
	users_stats.append(obj)
	count = count + 1
      else:
	for user in users_stats:
	  #print(user["email"])
	  if user["email"] == auth_report.email:
	    user["count"] = user["count"] + 1

    users_stats.sort(key=get_auth_count,reverse=True)
    print(users_stats)
    
    # pay_bill_reports
    pay_bill_reports = PayBillReport.objects.all()
    successful_pay_bill_count = PayBillReport.objects.filter(status=True).count()
    unsuccessful_pay_bill_count = PayBillReport.objects.filter(status=False).count()
    pay_bill_count = pay_bill_reports.count()
    
    # change_account_reports
    change_account_reports = ChangeAccountReport.objects.all()
    successful_change_account_count = ChangeAccountReport.objects.filter(status=True).count()
    unsuccessful_change_account_count = ChangeAccountReport.objects.filter(status=False).count()
    change_account_count = change_account_reports.count()
    
    template = loader.get_template('dashboard/dashboard.html')
    context = {
      'auth_reports' : auth_reports,
      'pay_bill_reports' : pay_bill_reports,
      'change_account_reports' : change_account_reports,
      
      'auth_count' : auth_count,
      'successful_auth_count' : successful_auth_count,
      'unsuccessful_auth_count' : unsuccessful_auth_count,
      'top_user_email' : json.dumps(users_stats[0]["email"]),
      'top_user_count' : json.dumps(users_stats[0]["count"]),
      
      'pay_bill_count' : pay_bill_count,
      'successful_pay_bill_count' : successful_pay_bill_count,
      'unsuccessful_pay_bill_count' : unsuccessful_pay_bill_count,
      
      'change_account_count' : change_account_count,
      'successful_change_account_count' : successful_change_account_count,
      'unsuccessful_change_account_count' : unsuccessful_change_account_count,
    }
    return HttpResponse(template.render(context, request))
  else:
    return redirect('index')
  
@csrf_exempt
def auth_report(request):
  
  try:
    if request.method == 'POST':
      print(request.POST["status"])
      #print(request.body)
      
      jsonn = {}
      if (str(request.POST["status"]) == "True") or (str(request.POST["status"]) == "False"):
	jsonn["email"] = request.POST["email"]
	jsonn["status"] = request.POST["status"]
     # else:
      #jsonn = json.loads(request.body)
      print(jsonn)
      
      email = jsonn["email"]
      status = jsonn["status"]
      
      
      is_valid_email = check_email(email)
      is_valid_status = check_status(status)
      
      print(email)
      print(status)
      print(is_valid_email)
      print(is_valid_status)
      
	
      if (is_valid_status == 0) or (is_valid_email == 0):
	return HttpResponse("NOT OK")
      else:
	print(request)
	auth_report_instance = AuthReport.objects.create(email=email,status=status)
	return HttpResponse("OK")
  except:
    return HttpResponse("NOT OK")
  
@csrf_exempt
def pay_bill_report(request):
  
  try:
    if request.method == 'POST':
      print(request.POST)
      
      jsonn = json.loads(request.body)
      print(jsonn)
      
      personal_account = jsonn["personal_account"]
      rate = jsonn["rate"]
      reading = jsonn["reading"]
      status = jsonn["status"]
      
      is_valid_account = check_personal_account(personal_account)
      is_valid_status = check_status(status)
      
	
      if (is_valid_account == 0) or (is_valid_status == 0):
	return HttpResponse("NOT OK")
      else:
	print(request)
	auth_report_instance = PayBillReport.objects.create(personal_account=personal_account,rate=rate,reading=reading,status=status)
	return HttpResponse("OK")
  except:
    return HttpResponse("NOT OK")
  
@csrf_exempt
def change_account_report(request):
  
  try:
    if request.method == 'POST':
      print(request.POST)
      
      jsonn = json.loads(request.body)
      print(jsonn)
      
      old = jsonn["old"]
      new = jsonn["new"]
      status = jsonn["status"]
      
      is_valid_old = check_personal_account(old)
      is_valid_new = check_personal_account(new)
      is_valid_status = check_status(status)
      
	
      if (is_valid_old == 0) or (is_valid_status == 0) or (is_valid_new == 0):
	return HttpResponse("NOT OK")
      else:
	print(request)
	auth_report_instance = ChangeAccountReport.objects.create(old=old,new=new,status=status)
	return HttpResponse("OK")
  except:
    return HttpResponse("NOT OK")
