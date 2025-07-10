
# serializers.py
from rest_framework import serializers
from .models import Classroom, Student, Attendance, AssessmentPoint, AssessmentRecord


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class ClassroomSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'students']  # tambahkan field lain jika ada


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class AssessmentPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPoint
        fields = '__all__'

class AssessmentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentRecord
        fields = '__all__'

