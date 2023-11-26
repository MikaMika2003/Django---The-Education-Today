from collections import Counter
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.urls import reverse
from account.forms import AccountForm, CreateUserForm, PostForm, UpdatePostForm, EditProfileForm, AddReplyForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
 # New
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from account.models import Account, Posts, Replies
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from teachers.models import Course, Grade, Question, Quiz, Student_Course
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        posts = Posts.objects.filter(title__contains=searched)
        quizzes = Quiz.objects.filter(title__contains=searched)
        posts_body = Posts.objects.filter(body__contains=searched)
        posts_snippet = Posts.objects.filter(snippet__contains=searched)

        course_name = Course.objects.filter(subject_name__contains=searched)

        context = {'searched': searched, 'posts': posts, 'quizzes': quizzes, 'posts_body': posts_body, 'posts_snippet': posts_snippet, 'course_name': course_name}

        return render(request, 'students/search.html', context)
    else:
        return render(request, 'students/search.html', {})

#Courses
@login_required(login_url='signin')
def courses(request):
    if request.user.account.is_teacher:
        courses = Course.objects.filter(teacher=request.user).order_by('name')
    else:
        courses = Student_Course.objects.filter(student=request.user).order_by('course')

    return render(request, 'students/courses.html', {'courses': courses})

@login_required(login_url='signin')
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    student = request.user

    is_enrolled = Student_Course.objects.filter(student=student, course=course)

    if is_enrolled:
        # Retrieve content related to the course
        posts = Posts.objects.filter(course=course)
        quizzes = Quiz.objects.filter(course=course)

        return render(request, 'students/course_detail.html', {
            'course': course,
            'posts': posts,
            'quizzes': quizzes
        })
    

    return render(request, 'students/course.html')


# Create your views here.
@login_required(login_url='signin')
def students_home(request):

    return render(request, 'students/main.html')

class UserEditPage(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'students/edit_profile.html'
    success_url = reverse_lazy('students:main')

    def get_object(self):
        return self.request.user

# Post Views
class PostsPage(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'students/posts.html' 
    login_url = '/signin/' 
    redirect_field_name = 'next'
    ordering = ['-post_date']

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')  # Adjust this to match your URL configuration
        queryset = Posts.objects.filter(course_id=course_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        context['course'] = course
        return context
    
    #success_url = reverse_lazy('students:posts')

    
class ArticlePage(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = 'students/article_detail.html' 
    login_url = '/signin/' 
    redirect_field_name = 'next'


class AddPostPage(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = PostForm
    template_name = 'students/add_post.html'
    login_url = '/signin/' 
    redirect_field_name = 'next'

    def form_valid(self, form):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        course_id = self.kwargs.get('course_id')
        return reverse('students:posts', kwargs={'course_id': course_id})


class AddReplyPage(LoginRequiredMixin, CreateView):
    model = Replies
    form_class = AddReplyForm
    template_name = 'students/add_comment.html'
    login_url = '/signin/' 
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


    success_url = reverse_lazy('students:posts')
    


class UpdatePostPage(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = UpdatePostForm
    template_name = 'students/update_post.html'
    login_url = '/signin/' 
    redirect_field_name = 'next'
    success_url = reverse_lazy('students:posts')
   

class DeletePostPage(LoginRequiredMixin, DeleteView):
    model = Posts
    template_name = 'students/delete_post.html'
    success_url = reverse_lazy('posts')
    login_url = '/signin/' 
    redirect_field_name = 'next'
    success_url = reverse_lazy('students:posts')

class PasswordsChangePage(LoginRequiredMixin, PasswordChangeView):
    from_class = PasswordChangeForm
    template_name = "students/change_password.html"
    success_url = reverse_lazy('students:password_success')


def password_success(request):
    return render(request, 'students/password_success.html', {})


def quizList(request, course_id):
    course = Course.objects.get(pk=course_id)
    quizzes = Quiz.objects.filter(course=course).order_by('-date_added')

    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(title = title, author=request.user, course=course)
        return redirect(reverse('students:quiz_list', args=[course_id]))
        
    context = {'quizzes': quizzes, 'course': course, }
    return render(request, "students/quiz_list.html", context)


def quizView(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)


    max_score = sum(question.points for question in questions)
    

    # Retrieve the latest grade, if it exists
    try:
        grade = Grade.objects.filter(quiz=quiz, student=request.user).latest('date_added')
    except Grade.DoesNotExist:
        grade = None
    
    max_attempts = 3
    quiz.weight = max_score
    quiz.save()

    if request.method == 'POST':
        if grade and grade.attempts >= max_attempts:
            # If they've exceeded the max_attempts, set the attempts to 0 to allow them to retake the quiz
            grade.attempts = 0
            grade.save()

        score = 0  # Initialize the score variable outside the loop
        correct = 0
        wrong = 0
        for question in questions:
            selected_answer = int(request.POST.get(f"{question.id}"))
            if selected_answer == question.ans:
                correct += 1
                score += question.points
            else:
                wrong += 1
        total = score / max_score * 100
        print(f"max_possible_score: {max_score}")

        # Calculate the user's total score
        #score = sum(question.points for question in questions if selected_answer == question.ans)
        #print(f" Score: {score}")
        #total = score/max_score * 100


        # Update the attempts field and create a new Grade instance
        if grade is None:
            Grade.objects.create(grade=total, quiz=quiz, student=request.user, attempts=1, user_score=score)
        else:
            # Only update the grade if the new grade is higher
            if total > grade.grade:
                grade.grade = total
                grade.user_score = score
                
            grade.attempts += 1
            grade.save()

        

        return redirect(reverse('students:quiz_view', args=[id]))


    remaining_attempts = max_attempts - (grade.attempts if grade else 0)

    context = {
        "questions": questions, 
        "quiz": quiz, 
        "grade": grade, 
        "remaining_attempts": remaining_attempts, 
        "max_score": max_score,
    }
    return render(request, "students/quiz_view.html", context)

def grades(request, course_id):
    course = Course.objects.get(pk=course_id)
    quizzes = Quiz.objects.filter(course=course).order_by('-date_added')
    grades = Grade.objects.filter(quiz__in=quizzes, student=request.user).order_by('quiz__date_added')
    
    max_score = 0
    for quiz in quizzes:
        max_score += quiz.weight
    print(f"max_score: {max_score}")

    overall_score = sum(grade.user_score for grade in grades)
    #max_possible_score = sum(grade.max_score for grade in grades)

    #overall_grade = (overall_score/max_possible_score)*100
    overall_grade = round((overall_score/max_score)*100, 2)
    print(f"overall percentage: {overall_grade}")

    # Calculate the student's percentile
    all_students_grades = [grade.grade for grade in Grade.objects.filter(quiz__in=quizzes).exclude(student=request.user)]
    student_percentile = round(calculate_percentile(overall_grade, all_students_grades),2)

    # Calculate the counts of each letter grade
    letter_grades = [get_letter_grade(grade.grade) for grade in grades]
    letter_grade_counts = dict(Counter(letter_grades))

    grade_count = grades.count()

    context = {
        "course": course, 
        "quizzes": quizzes, 
        "grades": grades,
        "overall_score": overall_score,
        #"max_possible_score": max_possible_score,
        "max_score": max_score,
        "overall_grade": overall_grade,
        "letter_grade_counts": letter_grade_counts,
        "student_percentile": student_percentile,
        "grade_count": grade_count,
    }
    return render(request, "students/grades.html", context)

def get_letter_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"
    
def calculate_percentile(value, data):
    """
    Calculate the percentile of a value in a dataset.
    """
    count_below = sum(1 for x in data if x <= value)
    return (count_below / len(data)) * 100 if data else 0

def past_courses(request):

    return render(request, "students/past_courses.html")

'''def grades(request, grade_id):
    grade = Grade.objects.get(pk=grade_id)
    max_attempts = 3  # Set this to the maximum number of attempts allowed


    context = {"grade": grade, "max_attempts": max_attempts}
    return render(request, "students/grades.html", context)'''


