import datetime
import time
from rest_framework.response import Response

from django.shortcuts import render
from rest_framework.views import APIView
from parking.models import Camera, Passport, Record


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
    ip_address = data.get('AlarmInfoPlate').get('ipaddr')
    camera = Camera.objects.get(ip_address=ip_address)
    car_id = data.get('AlarmInfoPlate').get('result').get('PlateResult').get('license')
    record = Record(
        car_id=car_id,
        camera=camera,
        record_date=datetime.datetime.now(),
        image_in_base64=data.get('AlarmInfoPlate').get('result').get('PlateResult').get('imageFile'),
        is_in=False
    )
    record.save()
    resp = {
        'license': car_id,
        'type': 'record_saved'
    }
    return resp
    pass


class HeartBeatHandler(APIView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        if 'form-data' in request.content_type:
            resp = handle_heartbeat(data)
        else:
            resp = handle_recognize(request.data)
        if 'serialno' in resp:
            time.sleep(10)
        print(resp)
        return Response(resp)
