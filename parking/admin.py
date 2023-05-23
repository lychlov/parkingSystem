from django.contrib import admin

from .models import Project, Manager, Camera, Record, Passport,Role

# Register your models here.

admin.site.register(Project)
admin.site.register(Manager)
admin.site.register(Camera)
admin.site.register(Record)
admin.site.register(Passport)
admin.site.register(Role)
