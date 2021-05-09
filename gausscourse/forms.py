from django import forms

class FilterForm(forms.Form):
    name_filter = forms.CharField(max_length=100, required=False)

class GradeForm(forms.Form):
    grade = forms.IntegerField()
    course_group_pk = forms.IntegerField()
    button = forms.CharField(max_length=10, required=True)
