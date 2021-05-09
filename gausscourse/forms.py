from django import forms

class FilterForm(forms.Form):
    name_filter = forms.CharField(max_length=100, required=False)

class GradeForm(forms.Form):
    grade = forms.IntegerField()
    select_course_group = forms.Select
