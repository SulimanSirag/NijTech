from django.conf.urls import url, include
from django.conf import settings

from mysite.personnel.api import views
from mysite.api import routers

urlpatterns = []
router = routers.PersonnelRouter()

router.register(r'areagroups',
                views.AreaGroupViewSet, base_name="areagroups")

router.register(r'department', views.SimpleDepartmentViewSet)
router.register(r'position', views.SimplePositionViewSet)
router.register(r'employee', views.SimpleEmployeeViewSet)

router.register(r'departments',
                views.DepartmentViewSet, base_name="departments")
department_routers = routers.nested_routers.NestedSimpleRouter(router, r'departments', lookup='department')
department_routers.register(r'employees', views.DepartmentEmployeeViewSet, base_name='department_employees')
department_routers.register(r'resigns', views.DepartmentResignViewSet, base_name='department_resigns')
urlpatterns.append(url(r'^', include(department_routers.urls)))

router.register(r'areas',
                views.AreaViewSet, base_name="areas")
area_routers = routers.nested_routers.NestedSimpleRouter(router, r'areas', lookup='area')
area_routers.register(r'employees', views.AreaEmployeeViewSet, base_name='area_employees')
area_routers.register(r'resigns', views.AreaResignViewSet, base_name='area_resigns')
urlpatterns.append(url(r'^', include(area_routers.urls)))

router.register(r'positions',
                views.PositionViewSet, base_name="positions")
position_routers = routers.nested_routers.NestedSimpleRouter(router, r'positions', lookup='position')
position_routers.register(r'employees', views.PositionEmployeeViewSet, base_name='position_employees')
position_routers.register(r'resigns', views.PositionResignViewSet, base_name='position_resigns')
urlpatterns.append(url(r'^', include(position_routers.urls)))

router.register(r'employees',
                views.EmployeeViewSet, base_name="employees")
router.register(r'employees_by_emp_code',
                views.EmployeeByEmpCodeView, base_name="employees_by_emp_code")
router.register(r'emp_data',
                views.EmployeeCreateViewSet, base_name="emp_data")
router.register(r'resigns',
                views.ResignViewSet, base_name="resigns")

router.register(r'employee_certifications',
                views.EmployeeCertificationViewSet, base_name="employeecertifications")


api_docs_urls_list = []
api_docs_urls_display_list = ['departments', 'areas', 'positions', 'employees', 'resigns']
if not settings.SHOW_ALL_API_DOCS:
    for each_url in router.urls:
        if each_url.name.split('-')[0] in api_docs_urls_display_list:
            api_docs_urls_list.append(each_url)
else:
    api_docs_urls_list = router.urls

personnel_api_docs_urls = [
    url(r'^', include(api_docs_urls_list)),
]

urlpatterns.append(url(r'^', include(router.urls)))
