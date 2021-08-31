from django.shortcuts import render, redirect
from .models import Opposum, Toy
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
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
  toys_opposum_doesnt_have = Toy.objects.exclude(id__in = opposum.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'opposums/detail.html', { 'opposum': opposum, 'feeding_form': feeding_form, 'toys': toys_opposum_doesnt_have })

class OpposumCreate(CreateView):
  model = Opposum
  fields = ['name', 'breed', 'description', 'age']

class OpposumUpdate(UpdateView):
  model = Opposum
  fields = ['breed', 'description', 'age']

class OpposumDelete(DeleteView):
  model = Opposum
  success_url = '/opposums/'

def add_feeding(request, opposum_id):
   # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the opposum_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.opposum_id = opposum_id
    new_feeding.save()
  return redirect('opposums_detail', opposum_id=opposum_id)

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, opposum_id, toy_id):
  Opposum.objects.get(id=opposum_id).toys.add(toy_id)
  return redirect('opposums_detail', opposum_id=opposum_id)