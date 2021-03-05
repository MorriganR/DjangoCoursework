from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=512)
    start_date = models.DateTimeField('date started')
    finish_date = models.DateTimeField('date finished')
    def __str__(self):
        return self.name

class CourseGroup(models.Model):
    name = models.CharField(max_length=512)
    curator = models.CharField(max_length=512)
    quantity_st = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.name + " - " + self.curator
