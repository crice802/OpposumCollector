from django.shortcuts import render
from .models import Opposum
# Create your views here.

#home view
def home(request):
  return render(request, 'home.html')
def about(request):
  return render(request, 'about.html')

def opposums_index(request):
  opposums = Opposum.objects.all()
  return render(request, 'opposums/index.html', { 'opposums': opposums })

def opposums_detail(request, opposum_id):
  opposum = Opposum.objects.get(id=opposum_id)
  return render(request, 'opposums/detail.html', { 'opposum': opposum })