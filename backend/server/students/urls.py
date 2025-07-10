from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'students', StudentViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'assessment-points', AssessmentPointViewSet)
router.register(r'assessment-records', AssessmentRecordViewSet)

urlpatterns = [
    path('students/search/', search_students, name='search_students'), 
    path('attendances/today/', today_attendance, name='today_attendance'), 
    path('attendances/by-student/', attendance_by_student),
]

urlpatterns += router.urls 
