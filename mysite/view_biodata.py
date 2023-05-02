from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mysite.personnel.models import Employee
from mysite.personnel.api import serializers
from mysite.iclock.models import BioData

class BiodataCreateOrUpdate(APIView):
    """
    create a new biodata.
    """


     def post(self, request, format=None):
        serializer = serializers.BioDataCreateSerializer(data=request.data)
        emp_code  = request.data.get('employee', None)
        if serializer.is_valid():
            data = serializer.data
            bio_no = data.get('bio_no', None)
            bio_tmp = data.get('bio_tmp', None)
            major_ver = data.get('major_ver', None)
            minor_ver = data.get('minor_ver', None)
            try:
                emp_id =  Employee.objects.get(emp_code=emp_code).id
                obj, created = BioData.objects.update_or_create(
                    employee_id=emp_id,
                    bio_no=bio_no,
                    bio_type = 1,
                    major_ver=major_ver,
                    minor_ver=minor_ver,
                    defaults={
                        "bio_tmp" : bio_tmp
                    })
                data['employee']  = emp_code
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
