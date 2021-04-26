from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('local/login', auth_views.LoginView.as_view()),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("login", views.login, name="login"),
    path("home", views.home, name="home"),
    path('', views.CourseIndexView.as_view(), name='index'),
]
