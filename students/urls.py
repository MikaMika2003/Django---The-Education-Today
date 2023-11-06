from django.urls import path, re_path
from . import views
from .views import ArticlePage, PostsPage, AddPostPage, UpdatePostPage, DeletePostPage, UserEditPage, PasswordsChangePage, AddReplyPage
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name='students'


urlpatterns = [
    path('', views.students_home, name="main"),

    # Posts
    path('article/<int:pk>/', views.ArticlePage.as_view(), name="article-detail"),
    path('courses/<int:course_id>/posts/', PostsPage.as_view(), name="posts"),
    path('courses/<int:course_id>/add_post/', AddPostPage.as_view(), name="add_post"),
    path('article/edit/<int:pk>', UpdatePostPage.as_view(), name="update_post"),
    path('article/<int:pk>/remove', DeletePostPage.as_view(), name="delete_post"),
    path('article/<int:pk>/add_reply/', AddReplyPage.as_view(), name="add_reply"),

    
    # User and passwords
    path('edit_profile/', UserEditPage.as_view(), name="edit_profile"),
    path('password/', PasswordsChangePage.as_view(), name="change_password"),
    path('password_success', views.password_success, name="password_success"),

    # Quiz and lessons
    path("quiz_list/", views.quizList, name="quiz_list"),
    path("quiz_view/<str:id>/", views.quizView, name="quiz_view"),
    path('grades/<int:grade_id>/', views.grades, name="grades"),

    #Courses
    path('courses/', views.courses, name="courses"),
    path('courses/<int:course_id>/', views.course_detail, name="course_detail"), 

    #Search 
    path('search', views.search, name="search"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)