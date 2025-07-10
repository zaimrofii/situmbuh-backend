# views.py
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Classroom, Student, Attendance, AssessmentPoint, AssessmentRecord
from .serializers import *

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        classroom = self.get_object()
        students = classroom.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


def search_students(request):
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all
    data = [
        {
            "id": s.id,
            "name": s.name,
            "classroom": s.classroom.name,
            "birth_date": s.birth_date,
            "gender": s.gender,
        }
        for s in students
    ]
    return JsonResponse(data, safe=False)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


@api_view(['GET'])
def today_attendance(request):
    now = datetime.now()  # naive datetime
    today = now.date()
    tomorrow = today + timedelta(days=1)

    data = Attendance.objects.filter(
        date__gte=today,
        date__lt=tomorrow
    ).order_by('time')
    serializer = AttendanceSerializer(data, many=True)
    return Response(serializer.data)
def attendance_by_student(request):
    student_id = request.query_params.get('student')
    if not student_id:
        return Response({"error": "student id required"}, status=400)

    data = Attendance.objects.filter(student_id=student_id).order_by('-date')
    serializer = AttendanceSerializer(data, many=True)
    return Response(serializer.data)


class AssessmentPointViewSet(viewsets.ModelViewSet):
    queryset = AssessmentPoint.objects.all()
    serializer_class = AssessmentPointSerializer

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AssessmentRecordViewSet(viewsets.ModelViewSet):
    queryset = AssessmentRecord.objects.all()
    serializer_class = AssessmentRecordSerializer

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

