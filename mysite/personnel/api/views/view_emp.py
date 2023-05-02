
import datetime

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mysite.api import mixin
from mysite.personnel.api import serializers
from mysite.personnel.api.filters import EmployeeListFilter
from mysite.personnel.api.utils_class import UtilGenericViewSet, SimpleViewSet
from mysite.personnel.models.model_department import Department
from mysite.personnel.models.model_employee import Employee



from rest_framework import viewsets

class EmployeeCreateViewSet(viewsets.ModelViewSet):
    """ Employee create view set """

    serializer_class = serializers.EmployeeCreateSerializer
    queryset = Employee.objects.all()



    def post(self, request):
        try:
            dept_name = request.data.pop('custom_dept_name', None)
            if dept_name:
                request.data['department']['dept_name'] = dept_name
            serializer = serializers.EmployeeCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeByEmpCodeView(viewsets.ModelViewSet):
    """ GET AND UPDATE EMPLOYEE"""
    serializer_class = serializers.EmployeeCreateSerializer
    lookup_field = 'emp_code'

    def get_queryset(self):
        return Employee.objects.all()

    def get(self, request, emp_code):
        try:
            employee = self.get_object()
            serializer = self.serializer_class(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, emp_code):
        try:
            dept_name = request.data.pop('custom_dept_name', None)
            if dept_name:
                request.data['department']['dept_name'] = dept_name
            employee = self.get_object()
            serializer = self.serializer_class(employee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
