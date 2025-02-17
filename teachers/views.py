from collections import Counter
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from account.forms import PostForm, UpdatePostForm, EditProfileForm, AddReplyForm
from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from account.models import Account, Posts, Replies
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from teachers.models import Course, Grade, Question, Quiz, Student_Course
from django.db.models import Avg, Max, Min, Q

# Create your views here.

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        # Search in the Account model for users
        users = Account.objects.filter(
            Q(username__icontains=searched) |  # Search by username
            Q(first_name__icontains=searched) |  # Search by first name
            Q(last_name__icontains=searched)  # Search by last name
            # Add more fields as needed
        )

        posts = Posts.objects.filter(title__contains=searched)
        quizzes = Quiz.objects.filter(title__contains=searched)
        posts_body = Posts.objects.filter(body__contains=searched)
        posts_snippet = Posts.objects.filter(snippet__contains=searched)
        course_name = Course.objects.filter(subject_name__contains=searched)

        context = {
            'searched': searched, 
            'posts': posts, 
            'quizzes': quizzes, 
            'posts_body': posts_body, 
            'posts_snippet': posts_snippet, 
            'course_name': course_name,
            "users": users,
            }
        
        return render(request, 'teachers/search.html', context)
    else:                        
        return render(request, 'teachers/search.html', {})
    

#Courses
@login_required(login_url='signin')
def courses(request):
    if request.user.account.is_teacher:
        courses = Course.objects.filter(teacher=request.user).order_by('name')
    else:
        courses = Student_Course.objects.filter(student=request.user)

     

    return render(request, 'teachers/courses.html', {'courses': courses})

@login_required(login_url='signin')
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = request.user

    students = Student_Course.objects.filter(course=course_id)
    # Count the number of students
    num_students = students.count()

    is_enrolled = Course.objects.filter(teacher=teacher, name=course)

    if is_enrolled:
        # Retrieve content related to the course
        posts = Posts.objects.filter(course=course)
        quizzes = Quiz.objects.filter(course=course)

        return render(request, 'teachers/course_detail.html', {
            'course': course,
            'posts': posts,
            'quizzes': quizzes,
            'students': students,
            'num_students': num_students,
        })
    else:
        return render(request, 'teachers/course.html')


#Home
@login_required(login_url='signin')
def teachers_home(request):

    return render(request, 'teachers/main.html')

class UserEditPage(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'teachers/edit_profile.html'
    success_url = reverse_lazy('teachers:main')

    def get_object(self):
        return self.request.user

# Post Views
class PostsPage(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'teachers/posts.html' 
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
    
    
class ArticlePage(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = 'teachers/article_detail.html' 
    login_url = '/signin/' 
    redirect_field_name = 'next'



class AddPostPage(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = PostForm
    template_name = 'teachers/add_post.html'
    login_url = '/signin/' 
    redirect_field_name = 'next'

    def form_valid(self, form):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        course_id = self.kwargs.get('course_id')
        return reverse('teachers:posts', kwargs={'course_id': course_id})

    
class AddReplyPage(LoginRequiredMixin, CreateView):
    model = Replies
    form_class = AddReplyForm
    template_name = 'teachers/add_comment.html'
    login_url = '/signin/' 
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('teachers:posts')
    
    
class UpdatePostPage(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = UpdatePostForm
    template_name = 'teachers/update_post.html'
    login_url = '/signin/' 
    redirect_field_name = 'next'
    success_url = reverse_lazy('teachers:posts')



class DeletePostPage(LoginRequiredMixin, DeleteView):
    model = Posts
    template_name = 'teachers/delete_post.html'
    success_url = reverse_lazy('posts')
    login_url = '/signin/' 
    redirect_field_name = 'next'
    success_url = reverse_lazy('teachers:posts')

class PasswordsChangePage(LoginRequiredMixin, PasswordChangeView):
    from_class = PasswordChangeForm
    template_name = "teachers/change_password.html"
    success_url = reverse_lazy('teachers:password_success')


def password_success(request):
    return render(request, 'teachers/password_success.html', {})

# Quizzes

def quizList(request, course_id):
    course = Course.objects.get(pk=course_id)
    quizzes = Quiz.objects.filter(course=course).order_by('-date_added')

    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(title = title, author=request.user, course=course)
        return redirect(reverse('teachers:quiz_list', args=[course_id]))
        
    context = {'quizzes': quizzes, 'courses': courses}
    return render(request, "teachers/quiz_list.html", context)

def quiz(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    grades = Grade.objects.filter(quiz=quiz)
    course = quiz.course
    

    # Calculate additional data for display
    highest_score = round(grades.aggregate(Max('grade'))['grade__max'], 2)
    lowest_score = round(grades.aggregate(Min('grade'))['grade__min'],2)
    average_score = round(grades.aggregate(Avg('grade'))['grade__avg'], 2)

    # Sorting logic
    sort_option = request.GET.get('sort', '')
    if sort_option == 'asc':
        sorted_grades = grades.order_by('grade')
    elif sort_option == 'desc':
        sorted_grades = grades.order_by('-grade')
    else:
        sorted_grades = grades

    # Calculate the counts of each letter grade
    letter_grades = [get_letter_grade(grade.grade) for grade in grades]
    letter_grade_counts = dict(Counter(letter_grades))
    grade_count = grades.count()
        
    context = {
        "quiz": quiz,
        "grades": sorted_grades,
        "course": course,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "average_score": average_score,
        "letter_grade_counts": letter_grade_counts,
        "grade_count": grade_count,
    }
    #context = {"quiz":quiz, "grades":grades, "course": course}
    return render(request, "teachers/quizzes.html", context)

def quizView(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        question = request.POST.get('question_text')
        op1 = request.POST.get('op1')
        op2 = request.POST.get('op2')
        op3 = request.POST.get('op3')
        op4 = request.POST.get('op4')
        ans = request.POST.get('ans')
        points = request.POST.get('points')

        print(f"Points: {points}")
        quiz.weight += int(points)
        quiz.save()

        Question.objects.create(
            quiz=quiz, question_text=question, op1=op1, op2=op2, op3=op3, op4=op4, ans=ans, points=points,
        )



        return redirect(reverse('teachers:quiz_view', args=[id]))
    context = {"questions":questions, "quiz":quiz}
    return render(request, "teachers/quiz_view.html", context)

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

'''def deleteQuiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    quiz.delete()
    return redirect(reverse('teachers:quiz_list'))'''

