from django.shortcuts import render
from .models import Opposum
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
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
  print(opposum)
  return render(request, 'opposums/detail.html', { 'opposum': opposum })

class OpposumCreate(CreateView):
  model = Opposum
  fields = ['name', 'breed', 'description', 'age']

class OpposumUpdate(UpdateView):
  model = Opposum
  fields = ['breed', 'description', 'age']

class OpposumDelete(DeleteView):
  model = Opposum
  success_url = '/opposums/'