from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import os
from .models import Student
from .models import Question, Option
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib import messages
from .models import StExam

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_home')
        else:
            # Handle invalid login credentials
            return render(request, 'student/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'student/login.html')


def student_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            student = Student.objects.create(user=user)  # Create and associate the Student object
            login(request, user)  # Log in the user
            return redirect('student_home')
    else:
        form = UserCreationForm()
    return render(request, 'student/signup.html', {'form': form})

@login_required
def student_home(request):
    # Retrieve student name from the database or session
    try:
        student = Student.objects.get(user=request.user)  # Assuming you have a Student model with a foreign key to the User model
    except Student.DoesNotExist:
        # Handle the case when Student object does not exist for the logged-in user
        pass
    student_name = student.name  # Replace with the appropriate field name in the Student model
    upcoming_exams = student.exams.all()  # Replace with the appropriate field name in the Student model
    context = {
        'student_name': student_name,
        'upcoming_exams': upcoming_exams,
    }
    return render(request, 'student/student_home.html', context)


@login_required  # Require authentication for accessing the view
def student_exam(request):
    if request.method == 'POST':
        exam_id = request.POST['exam_id']
        # Retrieve the exam and associated questions from the database
        try:
            exam = StExam.objects.get(name=exam_id)
            
        except StExam.DoesNotExist:
            # Add an error message to the messages framework
            messages.error(request, 'Exam not found.')
            return redirect('student_home')

        # clean the question and options models
        Question.objects.filter(exam=exam).delete()

        # Read the questions and options from the text file
        # print(os.path.join(settings.BASE_DIR, 'exam_files', exam_id + '.txt'))
        file_path = os.path.join(settings.BASE_DIR, 'exam_files', exam_id + '.txt')
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Parse the lines to extract questions and options
        question_count = 0
        current_question = None
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                # Create a new Question object
                current_question = Question.objects.create(exam=exam, text=line[2:], question_id=question_count)
                # append options of previous question to options list and reset it
                question_count += 1
            elif line.startswith('A:'):
                # Create a new Option object for the current question
                option = Option.objects.create(text=line[2:], of_question_id=question_count)
                # Add the option to the current question
                current_question.options.add(option)

        questions = Question.objects.filter(exam=exam)

        context = {
            'exam_id': exam_id,
            'questions': questions,
        }
        return render(request, 'student/student_exam.html', context)

    else:
        # Process the submitted exam
        exam_id = request.POST['exam_id']
        # Retrieve the selected options for each question and save them in the database
        # for question in Question.objects.filter(exam = StExam.objects.get(name=exam_id)):
            # selected_option_id = request.POST.get('question' + str(question.question_id))
            # if selected_option_id:
            #     selected_option = Option.objects.get(of_question_id=selected_option_id)
                # Save the selected option for the question in the database
                

        # Perform any additional processing or validation as required

        # Redirect the student to a page after exam submission (e.g., a thank you page)
        return redirect('exam_submission_confirmation')
    
@login_required
def exam_submission_confirmation(request):
    return render(request, 'student/exam_submission_confirmation.html')
    
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('homepage'))
