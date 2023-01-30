from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def dashboard(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())

def copy(request):
    template = loader.get_template('copy.html')
    return HttpResponse(template.render())