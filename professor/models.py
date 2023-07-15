from django.db import models
from django.contrib.auth.models import User
# from student.models import Exam as StudentExam
from student.models import Student

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Anonymous')
    courses = models.ManyToManyField('Course')
    exams = models.ManyToManyField('Exam')

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='upcoming')

    def __str__(self):
        return self.name

