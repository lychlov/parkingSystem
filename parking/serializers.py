import re

from .models import Passport, Camera, Project, Record
from rest_framework import serializers


def is_car_id(value):
    # pattern_str = r"^([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[a-zA-Z](([DF]((?![IO])[a-zA-Z0-9](?![IO]))[0-9]{4})|([0-9]{5}[DF]))|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1})$"
    pattern_str = r"^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]"
    if not re.findall(pattern_str, value):
        raise serializers.ValidationError('车牌号无效.')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description')


class CameraSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Camera
        fields = ('id', 'project', 'ip_address', 'camera_type',)


class RecordSerializer(serializers.ModelSerializer):
    # car_id = serializers.CharField(max_length=255, validators=[is_car_id])
    camera = CameraSerializer(many=False, read_only=True)

    class Meta:
        model = Record
        fields = ('id', 'car_id', 'camera', 'record_date', 'image', 'is_in','image_in_base64')


class PassportSerializer(serializers.ModelSerializer):
    car_id = serializers.CharField(max_length=255, validators=[is_car_id])
    camera = CameraSerializer(many=False, read_only=True)

    class Meta:
        model = Passport
        fields = ('id', 'car_id', 'camera', 'enable_time', 'overdue_time', 'is_pushed', 'is_deleted')
