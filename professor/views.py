from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from proctoring_project.settings import BASE_DIR
from .models import Professor, Course, Exam
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import View
from student.models import StExam, Student

# import cv2
# import dlib

def homepage(request):
    return render(request, 'homepage.html')

def professor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('professor_home')
        else:
            # Handle invalid login credentials
            return render(request, 'professor/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'professor/login.html')


def professor_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            professor = Professor.objects.create(user=user)  # Create and associate the Professor object
            return redirect('professor_login')
    else:
        form = UserCreationForm()
    return render(request, 'professor/signup.html', {'form': form})

@login_required
def professor_home(request):
    # Retrieve professor information from the database or session
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        pass
    courses = professor.courses.all()
    upcoming_exams = professor.exams.all() #########################################
    
    context = {
        'professor': professor,
        'courses': courses,
        'upcoming_exams': upcoming_exams,
    }
    return render(request, 'professor/professor_home.html', context)

@login_required
def add_exam(request):
    if request.method == 'POST':
        exam_name = request.POST['exam_name']
        
        # Retrieve the Professor object associated with the current user
        professor = Professor.objects.get(user=request.user)
        
        # Create a new exam in the database with the provided exam_name and status
        exam = Exam.objects.create(name=exam_name, status='upcoming')
        
        # Add the exam to the exams ManyToManyField of the professor
        professor.exams.add(exam)
        
        # Get all the students from the database
        students = Student.objects.all()
        
        # Add the exam to each student
        for student in students:
            stexam = StExam.objects.create(name=exam_name, status='upcoming')
            student.exams.add(stexam)
            student.save()
        
        # Save the changes to the professor and students
        professor.save()
        
        
        # Redirect the professor to a confirmation page or any other desired page
        return redirect('professor_home')
    
    return render(request, 'add_exam.html')

@login_required
def proctor(request):
    # Get the path to the directory where the captured photos are stored
    photos_directory = os.path.join(BASE_DIR, 'static/photos')

    # Retrieve the list of captured photo filenames
    photos = []
    for filename in os.listdir(photos_directory):
        if filename.endswith('.jpg'):
            photo_path = os.path.join(photos_directory, filename)
            photos.append({
                'filename': filename,
                'url': photo_path,
            })

    exam_name = request.GET.get('exam_name')
    try:
        exam = Exam.objects.filter(name=exam_name, status='upcoming')
    except Exam.DoesNotExist:
        exam = None

    # Retrieve the Professor object associated with the current user
    professor = Professor.objects.get(user=request.user)
    # Pass the photos,exam variable to the template
    context = {
        'photos': photos,
        'exam': exam,
        'professor': professor,
    }
    return render(request, 'professor/proctor.html', context)

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('homepage'))
