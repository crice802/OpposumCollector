from django.shortcuts import render, redirect
from .models import Opposum, Toy, Photo
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'opposumcollector'
# Create your views here.

#home view
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def opposums_index(request):
  opposums = Opposum.objects.filter(user=request.user)
  return render(request, 'opposums/index.html', { 'opposums': opposums })

@login_required
def opposums_detail(request, opposum_id):
  opposum = Opposum.objects.get(id=opposum_id)
  toys_opposum_doesnt_have = Toy.objects.exclude(id__in = opposum.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'opposums/detail.html', { 'opposum': opposum, 'feeding_form': feeding_form, 'toys': toys_opposum_doesnt_have })

class OpposumCreate(LoginRequiredMixin, CreateView):
  model = Opposum
  fields = ['name', 'breed', 'description', 'age']
  # This inherited method is called when a
  # valid opposum form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the opposum
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class OpposumUpdate(LoginRequiredMixin, UpdateView):
  model = Opposum
  fields = ['breed', 'description', 'age']

class OpposumDelete(LoginRequiredMixin, DeleteView):
  model = Opposum
  success_url = '/opposums/'

@login_required
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

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, opposum_id, toy_id):
  Opposum.objects.get(id=opposum_id).toys.add(toy_id)
  return redirect('opposums_detail', opposum_id=opposum_id)

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('opposums_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)