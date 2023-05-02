
from rest_framework import serializers

from mysite.personnel.models.model_department import Department
from mysite.personnel.models.model_employee import Employee

class DepartmentField(serializers.Field):
    """Fields for Department"""
    
    def to_internal_value(self, data):
        if isinstance(data, dict):
            dept_code = data.get('dept_code')
            dept_name = data.get('dept_name')
            try:
                department = Department.objects.get(dept_code=dept_code)
                department.dept_name = dept_name
                department.save()
                return department
            except Department.DoesNotExist:
                department = Department.objects.create(dept_code=dept_code, dept_name=dept_name)
                return department


    def to_representation(self, obj):
        return {'dept_name': obj.dept_name, 'dept_code': obj.dept_code}


    
class EmployeeCreateSerializer(serializers.ModelSerializer):
    """ Represent  a Employee object """
    department = DepartmentField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'emp_code', 'first_name', 'last_name', 'nickname',
            'device_password', 'card_no', 'department', 'position', 'hire_date',
            'gender', 'birthday', 'verify_mode', 'emp_type',
            'dev_privilege',
            'self_password', 'flow_role', 'area',

            
        ]
