from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=512)
    start_date = models.DateTimeField('date started')
    finish_date = models.DateTimeField('date finished')
    is_public = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=512)
    curator = models.CharField(max_length=512)
    def __str__(self):
        return self.name

class CourseGroup(models.Model):
    name = models.CharField(max_length=512)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    is_rate_allowed = models.BooleanField(default=True)
    def __str__(self):
        return self.course.name + " - " + self.group.name

class MyUser(models.Model):
    name = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.name + " - " + self.user.get_full_name()

class Grade(models.Model):
    name = models.CharField(max_length=512)
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0)
    def __str__(self):
        return str(self.grade) + " - " + self.my_user.user.get_full_name() \
		+ " - " + self.course_group.course.name + " - " + self.course_group.group.name
