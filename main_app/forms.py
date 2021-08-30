from django.forms import ModelForm, fields
from .models import Feeding

class FeedingForm(ModelForm):
  class Meta:
    model = Feeding
    fields = ['date', 'meal']