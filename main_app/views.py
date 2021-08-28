from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#home view
def home(request):
  return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')

def about(request):
  return render(request, 'about.html')

def opposums_index(request):
  return render(request, 'opposums/index.html', { 'opposums': opposums })