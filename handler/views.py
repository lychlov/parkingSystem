import base64
import datetime
import os
import time

import pytz
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from parking.models import Camera, Passport, Record

MAX_DURATION = 15
MIN_DURATION = 10


def base64_2_file(base64_str, file_name):
    with open(file_name, 'wb') as f:
        f.write(base64.b64decode(base64_str))
    pass


def handle_heartbeat(data):
    ip_address = data.get('ipaddr')
    serial_no = data.get('serialno')
    resp = {'serialno': serial_no}
    camera = Camera.objects.get(ip_address=ip_address)
    add_passport = Passport.objects.filter(camera=camera, is_pushed=False, is_deleted=False).order_by('id')[:5]
    delete_passport = Passport.objects.filter(camera=camera, is_deleted=True, is_deleted_pushed=False).order_by('id')[:5]
    if add_passport:

        white_list_data = []
        for p in add_passport:
            temp = {
                "plate": p.car_id,  # "津AEM182",
                "enable": 1,
                "need_alarm": 0,
                "enable_time": p.enable_time.strftime('%Y-%m-%d %H:%M:%S'),  # "2023-05-01 11:11:11",
                "overdue_time": p.overdue_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            white_list_data.append(temp)
            p.is_pushed = True
            p.save()
        resp = {"Response_AlarmInfoPlate":
            {
                "white_list_operate":
                    {"operate_type": 0,
                     "white_list_data": white_list_data
                     }
            }
        }
    elif delete_passport:
        white_list_data = []
        for p in add_passport:
            temp = {
                "plate": p.car_id,
                "enable": 1,
                "need_alarm": 0
            }
            white_list_data.append(temp)
            p.is_deleted_pushed = True
            p.save()
        resp = {
            "Response_AlarmInfoPlate": {
                "white_list_operate":
                    {"operate_type": 1,
                     "white_list_data": white_list_data
                     }
            }
        }
    return resp


# Create your views here.
def handle_recognize(data):
    # print(data)

    serial_no = data.get('AlarmInfoPlate').get('serialno')
    camera = Camera.objects.get(serial_number=serial_no)
    car_id = data.get('AlarmInfoPlate').get('result').get('PlateResult').get('license')
    last_record = Record.objects.filter(camera=camera, car_id=car_id, is_valid=False, is_judged=False).last()
    now_date = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    image_in_base64 = data.get('AlarmInfoPlate').get('result').get('PlateResult').get('imageFile')
    file_name = '{}@{}@{}.png'.format(serial_no, car_id, now_date.strftime('%Y-%m-%d %H:%M:%S'))
    full_path = os.path.sep.join((settings.STATICFILES_DIRS[0], 'recognize_pics', file_name))
    base64_2_file(image_in_base64, full_path)
    # 有最近暂存记录
    if last_record:
        last_date = last_record.auto_first_date
        time_delta = now_date - last_date
        # 超时限：重新记录，上条记录归档
        if time_delta > datetime.timedelta(minutes=MAX_DURATION):
            last_record.is_valid = False
            last_record.is_judged = True
            last_record.save()
            new_record = Record(
                car_id=car_id,
                camera=camera,
                auto_first_date=now_date,
                auto_first_image_url=file_name,
                manual_first_image_url='',
                manual_second_image_url='',
                is_valid=False,
                is_judged=False
            )
            new_record.save()
            resp = {
                'license': car_id,
                'type': 'auto_first_record_saved'
            }
        else:
            # 手动第一次记录，归并存入
            if not last_record.manual_first_image_url:
                last_record.manual_first_date = now_date
                last_record.manual_first_image_url = file_name
                last_record.save()
                resp = {
                    'license': car_id,
                    'type': 'manual_first_record_saved'
                }
            # 手动第二次记录，归并存入，记录归档
            elif not last_record.manual_second_image_url:
                last_record.manual_second_date = now_date
                last_record.manual_second_image_url = file_name
                last_record.is_valid = time_delta > datetime.timedelta(minutes=MIN_DURATION)
                last_record.is_judged = True
                last_record.save()
                resp = {
                    'license': car_id,
                    'type': 'manual_second_record_saved'
                }
            else:
                print('记录处理意外，请注意')
                resp = {
                    'license': car_id,
                    'type': '记录处理意外，请注意'
                }
    # 无最近暂存记录
    else:
        new_record = Record(
            car_id=car_id,
            camera=camera,
            auto_first_date=now_date,
            auto_first_image_url=file_name,
            manual_first_image_url='',
            manual_second_image_url='',
            is_valid=False,
            is_judged=False
        )
        new_record.save()
        resp = {
            'license': car_id,
            'type': 'auto_first_record_saved'
        }
    return resp


class HeartBeatHandler(APIView):

    def post(self, request, *args, **kwargs):
        data = request.POST

        if 'form-data' in request.content_type:
            resp = handle_heartbeat(data)
        else:
            if 'AlarmInfoPlate' in request.data:
                resp = handle_recognize(request.data)
            else:
                resp = {'serialno': "noting to do"}
        if 'serialno' in resp:
            time.sleep(10)
        print(resp)
        return Response(resp)
