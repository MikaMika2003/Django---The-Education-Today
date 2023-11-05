from django.urls import path
from . import views
#from .views import UserEditPage#, FileFieldView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name='account'

urlpatterns = [
    path('', views.signin, name="signin"),
    #path('teachers_home/', views.teachers_home, name="main2"),

    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    #path('edit_profile/', UserEditPage.as_view(), name="edit_profile"),
    #path('18/password/', auth_views.PasswordChangeView.as_view(template_name='account/change_password.html')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)