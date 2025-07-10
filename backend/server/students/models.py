import uuid
from django.db import models

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, related_name='students', on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='attendances', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # otomatis isi tanggal saat absen dibuat
    time = models.TimeField(auto_now_add=True)  # otomatis isi waktu saat absen dibuat
    status = models.CharField(max_length=10, choices=[
        ('hadir', 'Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
        ('bolos', 'Bolos'),
    ])
    note = models.TextField(blank=True, null=True)



class AssessmentPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    
    # Kategori utama: motorik, kognitif, sosial, dll
    domain = models.CharField(
        max_length=50,
        choices=[
            ('motorik', 'Motorik'),
            ('kognitif', 'Kognitif'),
            ('bahasa', 'Bahasa'),
            ('sosial', 'Sosial'),
            ('emosional', 'Emosional'),
        ]
    )

    # Untuk membedakan indikator per kelas (jika dibutuhkan)
    classroom = models.ForeignKey(
        'Classroom',
        related_name='assessment_points',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.domain})"

class AssessmentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'Student',
        related_name='assessment_records',
        on_delete=models.CASCADE
    )
    
    point = models.ForeignKey(
        AssessmentPoint,
        related_name='records',
        on_delete=models.CASCADE
    )
    
    score = models.IntegerField()  # Skala bisa 1–5, atau 0–100
    note = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.point.name} ({self.score})"
