from django.contrib import admin
from .models import Opposum, Feeding, Toy, Photo


# Register your models here.
admin.site.register(Opposum)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)