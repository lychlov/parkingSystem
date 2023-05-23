import time

from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Camera(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    camera_type = models.CharField(max_length=255)

    def __str__(self):
        return '{}|{}'.format(self.name, self.ip_address)


class Passport(models.Model):
    car_id = models.CharField(max_length=255)
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
    enable_time = models.DateTimeField()
    overdue_time = models.DateTimeField()
    is_pushed = models.BooleanField()
    is_deleted = models.BooleanField()
    is_deleted_pushed = models.BooleanField(default=False)

    # create_time = models.DateTimeField(default=time.time())
    def __str__(self):
        return self.car_id


class Record(models.Model):
    car_id = models.CharField(max_length=255)
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
    record_date = models.DateTimeField(default=timezone.now())
    image = models.ImageField(upload_to='static/recognize_pics')
    image_in_base64 = models.TextField()
    is_in = models.BooleanField()

    def __str__(self):
        return "{}|{}".format(self.car_id, self.camera.name)


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project, related_name='projects')
    role = models.ForeignKey(to=Role, related_name='roles', on_delete=models.CASCADE)

    def __str__(self):
        return '{}|{}'.format(self.user.username, self.role.name)
