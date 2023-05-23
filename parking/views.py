import requests
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Passport, Manager, Camera, Record
from .serializers import PassportSerializer, CameraSerializer, RecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import datetime


# Create your views here.
class Login(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'code': 20000,
            'data': {'token': token.key},
        })


class UserInfo(APIView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        user = Token.objects.get(key=token).user
        manager = Manager.objects.get(user=user)
        return Response({
            'code': 20000,
            'data': {'roles': [manager.role.name],
                     'introduction': '',
                     'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                     'name': user.username, }
        })


class CameraList(APIView):
    def get(self, request, *args, **kwargs):
        # args:importance, type, title, page,limit = 20, sort

        user = request.user
        manager = Manager.objects.get(user=user)

        query = request.GET
        page = query.get('page', 1)  # 获取第几页
        limit = query.get('limit', 20)  # 每页有多少条数据
        title = query.get('title', '')
        projects = [x.id for x in manager.projects.all()]
        queryset = Camera.objects.filter(project_id__in=projects)
        data_list = []
        for i in queryset:
            mode_to = CameraSerializer(i).data  # exclude这个是转字典的时候去掉，哪个字段，就是不给哪个字段转成字典
            data_list.append(mode_to)
        resp = {
            'code': 20000,
            'data': {
                'total': queryset.count(),
                'items': data_list
            }
        }
        return Response(resp)


class RecordList(APIView):

    def get(self, request, *args, **kwargs):
        # args:importance, type, title, page,limit = 20, sort

        user = request.user
        manager = Manager.objects.get(user=user)

        query = request.GET
        page = query.get('page', 1)  # 获取第几页
        limit = query.get('limit', 20)  # 每页有多少条数据
        car_id = query.get('car_id', '')
        camera_id = query.get('camera_id', '')
        sort = query.get('sort', '')
        projects = [x.id for x in manager.projects.all()]
        queryset = Record.objects.filter(camera__project_id__in=projects)
        if car_id:
            infos = queryset.filter(car_id__contains=car_id)
        else:
            infos = queryset.all()
        if camera_id:
            infos = infos.filter(camera_id=camera_id)
        if sort == '-id':
            infos = infos.order_by(sort)
        paginator = Paginator(infos, limit)
        page_1 = paginator.get_page(page)
        data_list = []
        for i in page_1:
            mode_to = RecordSerializer(i).data
            # mode_to['image_fake'] = mode_to['image'].replace('/static/', '/static_base/') if mode_to['image'] else '' # exclude这个是转字典的时候去掉，哪个字段，就是不给哪个字段转成字典
            data_list.append(mode_to)
        resp = {
            'code': 20000,
            'data': {
                'total': infos.count(),
                'items': data_list
            }
        }
        return Response(resp)


class PassportList(APIView):

    def get(self, request, *args, **kwargs):
        # args:importance, type, title, page,limit = 20, sort

        user = request.user
        manager = Manager.objects.get(user=user)

        query = request.GET
        page = query.get('page', 1)  # 获取第几页
        limit = query.get('limit', 20)  # 每页有多少条数据
        car_id = query.get('car_id', '')
        camera_id = query.get('camera_id', '')
        sort = query.get('sort', '')
        projects = [x.id for x in manager.projects.all()]
        queryset = Passport.objects.filter(camera__project_id__in=projects)
        if car_id:
            infos = queryset.filter(car_id__contains=car_id)
        else:
            infos = queryset.all()
        if camera_id:
            infos = infos.filter(camera_id=camera_id)
        if sort == '-id':
            infos = infos.order_by(sort)

        paginator = Paginator(infos, limit)
        page_1 = paginator.get_page(page)
        data_list = []
        for i in page_1:
            mode_to = PassportSerializer(i).data  # exclude这个是转字典的时候去掉，哪个字段，就是不给哪个字段转成字典
            data_list.append(mode_to)
        resp = {
            'code': 20000,
            'data': {
                'total': infos.count(),
                'items': data_list
            }
        }
        return Response(resp)

    def put(self, request, *args, **kwargs):
        query = request.GET
        pk = int(query.get('pk', 1))
        item = Passport.objects.get(id=pk)
        item.is_deleted = False
        item.is_pushed = False
        item.save()
        return Response({
            'code': 20000,
            'data': 'success'
        })

    def delete(self, request, *args, **kwargs):
        query = request.GET
        pk = int(query.get('pk', 1))
        item = Passport.objects.get(id=pk)
        item.is_deleted = True
        item.is_pushed = False
        item.save()
        return Response({
            'code': 20000,
            'data': 'success'
        })

    def post(self, request, format=None):
        camera_id = request.data.get('camera_id')
        camera = Camera.objects.get(id=camera_id)
        item = {
            'car_id': request.data.get('car_id'),
            'camera_id': request.data.get('camera_id'),
            "camera": {'id': camera_id},
            "enable_time": request.data.get('enable_time'),
            "overdue_time": request.data.get('enable_time'),
            "is_pushed": False,
            "is_deleted": False,
        }
        serializer = PassportSerializer(data=item)
        if serializer.is_valid():
            new_item = Passport(
                car_id=request.data.get('car_id'),
                camera=camera,
                enable_time=request.data.get('enable_time'),
                overdue_time=request.data.get('overdue_time'),
                is_pushed=False,
                is_deleted=False
            )
            new_item.save()
            return Response(
                {'code': 20000,
                 'data': 'success',
                 'item': serializer.data
                 })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # class PassportList(generics.ListCreateAPIView):
    #     queryset = Passport.objects.all()
    #     serializer_class = PassportSerializer
    #     # permission_classes = [IsAuthenticatedOrReadOnly]
    #     authentication_classes = [TokenAuthentication]
    #     # authentication_classes = [SessionAuthentication, BasicAuthentication]
    #     permission_classes = [IsAuthenticated]
    #


class PassportDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PassportSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        passport = self.kwargs['pk']
        return Passport.objects.filter(id=passport)

    def delete(self, request, *args, **kwargs):
        passport = self.kwargs['pk']
        item = Passport.objects.get(id=passport)
        item.is_deleted = True
        item.save()
        return Response({
            'code': 20000,
            'data': 'success'
        })


#
# class PassportDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Passport.objects.get(pk=pk)
#         except Passport.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         passport = self.get_object(pk)
#         serializer = PassportSerializer(passport)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         passport = self.get_object(pk)
#         serializer = PassportSerializer(passport, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        camera = Camera.objects.count()
        passport = Passport.objects.count()
        record = Record.objects.count()
        today = Record.objects.filter(record_date__gt=(datetime.datetime.now()-datetime.timedelta(days=1))).count()
        resp = {
            'code': 20000,
            'status': True,
            'data': {'items': {
                'camera': camera,
                'passport': passport,
                'record': record,
                'today': today
            }},
        }
        return Response(resp)
