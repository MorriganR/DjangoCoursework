from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("home", views.home, name="home"),
    path('course/', views.course_detail, name='course'),
    path('course/<int:course_id>/', views.course_detail),
    path('', views.CourseIndexView.as_view(), name='index'),
    
]
