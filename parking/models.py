import time

from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    # description = models.TextField()
    token = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    provider_no = models.CharField(max_length=255)
    provider_address = models.CharField(max_length=255)
    provider_sign_date = models.DateTimeField()
    construction_name = models.CharField(max_length=255)
    total_no = models.CharField(max_length=255)
    total_name = models.CharField(max_length=255)

    pm_name = models.CharField(max_length=255)
    pm_phone = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    zone_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    complete_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    construct_size = models.CharField(max_length=255)
    construct_type = models.CharField(max_length=255)
    construct_usage = models.CharField(max_length=255)
    smj_name = models.CharField(max_length=255)
    smj_phone = models.CharField(max_length=255)
    smj_email = models.EmailField()
    jl_name = models.CharField(max_length=255)
    jl_phone = models.CharField(max_length=255)
    jl_corp_code = models.CharField(max_length=255)
    jl_corp_name = models.CharField(max_length=255)
    az_phone = models.CharField(max_length=255)
    create_time = models.DateTimeField(default=timezone.now())

    # project_no = models.CharField(max_length=255)
    # area_code = models.CharField(max_length=255)
    # supplier_name = models.CharField(max_length=255)
    # builder_license_umm = models.CharField(max_length=255)
    # contractor_corp_code = models.CharField(max_length=255)
    # contractor_corp_name = models.CharField(max_length=255)
    # corp_name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    # function_num = models.CharField(max_length=255)
    # jl_name = models.CharField(max_length=255)
    # jl_phone = models.CharField(max_length=255)
    # jlcorp_code = models.CharField(max_length=255)
    # jlcorp_name = models.CharField(max_length=255)
    # kf_area_code = models.CharField(max_length=255)
    # prj_name = models.CharField(max_length=255)
    # prj_size = models.CharField(max_length=255)
    # prj_status = models.CharField(max_length=255)
    # prmanager = models.CharField(max_length=255)
    # is_push = models.CharField(max_length=255, default='0')
    # property_num = models.CharField(max_length=255)
    # prphone = models.CharField(max_length=255)
    # register_date = models.DateTimeField(default=timezone.now())
    # smj_name = models.CharField(max_length=255)
    # smj_phone = models.CharField(max_length=255)
    # start_date = models.DateTimeField(default=timezone.now())
    # is_corp_push = models.CharField(max_length=255, default='0')
    # corp_code = models.CharField(max_length=255)
    # invest = models.CharField(max_length=255)
    # building_area = models.CharField(max_length=255)
    # az_phone = models.CharField(max_length=255)
    # remark = models.CharField(max_length=255)
    # update_type = models.CharField(max_length=255)
    # zb_date = models.DateTimeField(default=timezone.now())
    # zb_quxian = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Camera(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # ip_address = models.GenericIPAddressField()
    # camera_type = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)

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
    # record_date = models.DateTimeField(default=timezone.now())
    # image = models.ImageField(upload_to='static/recognize_pics')
    # image_in_base64 = models.TextField()
    auto_first_date = models.DateTimeField(default=timezone.now())
    auto_first_image_url = models.CharField(max_length=255)
    manual_first_date = models.DateTimeField(default=timezone.now())
    manual_first_image_url = models.CharField(max_length=255)
    manual_second_date = models.DateTimeField(default=timezone.now())
    manual_second_image_url = models.CharField(max_length=255)

    is_valid = models.BooleanField(default=False)
    is_judged = models.BooleanField(default=False)

    # is_in = models.BooleanField()

    def __str__(self):
        return "{}|{}".format(self.car_id, self.camera.name)


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project, related_name='projects', null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    work = models.CharField(max_length=255)
    role = models.ForeignKey(to=Role, related_name='roles', on_delete=models.CASCADE)

    def __str__(self):
        return '{}|{}'.format(self.user.username, self.role.name)
