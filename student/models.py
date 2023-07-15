from django.db import models
from django.contrib.auth.models import User
# from professor.models import StudentExam

class StExam(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='upcoming')

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Anonymous')
    exams = models.ManyToManyField(StExam)

    def __str__(self):
        return self.user.username
    
class Option(models.Model):
    of_question_id = models.IntegerField(default=0)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class Question(models.Model):
    question_id = models.IntegerField(default=0)
    exam = models.ForeignKey(StExam, on_delete=models.CASCADE)
    text = models.TextField()
    options  = models.ManyToManyField(Option)

    def __str__(self):
        return self.text
