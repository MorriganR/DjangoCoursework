from django.contrib import admin

# Register your models here.

from .models import Course, Group, CourseGroup, MyUser, Grade

admin.site.register(Course)
admin.site.register(Group)
admin.site.register(CourseGroup)
admin.site.register(MyUser)
admin.site.register(Grade)
