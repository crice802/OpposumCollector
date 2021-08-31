from django.shortcuts import render, redirect
from .models import Opposum, Toy, Photo
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'opposumcollector'
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

def add_photo(request, opposum_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to opposum_id or opposum (if you have a opposum object)
      photo = Photo(url=url, opposum_id=opposum_id)
      # Remove old photo if it exists
      opposum_photo = Photo.objects.filter(opposum_id=opposum_id)
      if opposum_photo.first():
        opposum_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('opposums_detail', opposum_id=opposum_id)