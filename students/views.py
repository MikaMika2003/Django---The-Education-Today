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

        results = Posts.objects.filter(title__contains=searched)
        quizzes = Quiz.objects.filter(title__contains=searched)

        return render(request, 'students/search.html', {'searched': searched, 'results': results, 'quizzes': quizzes})
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


def quizList(request):
    quizzes = Quiz.objects.order_by('-date_added')
    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(title = title, author=request.user)
        return redirect(reverse('students:quiz_list'))
        
    context = {'quizzes': quizzes}
    return render(request, "students/quiz_list.html", context)

def quizView(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)
    try:
        grade = Grade.objects.get(quiz=quiz, student=request.user)
    except ObjectDoesNotExist:
        grade = None
    
    if request.method == 'POST':
        total_questions = len(questions)
        correct = 0
        wrong = 0
        for question in questions:
            selected_answer = int(request.POST.get(f"{question.id}"))
            if selected_answer == question.ans:
                correct += 1
            else:
                wrong += 1
        total = correct/total_questions * 100
        Grade.objects.create(grade = total, quiz=quiz, student=request.user)

        messages.success(request, f'Correct: {correct}')
        messages.success(request, f'Wrong: {wrong}')

        return redirect(reverse('students:quiz_view', args=[id]))
    
    context = {"questions":questions, "quiz":quiz, "grade":grade}

    
    return render(request, "students/quiz_view.html", context)