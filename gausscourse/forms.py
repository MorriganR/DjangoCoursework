from django import forms

class FilterForm(forms.Form):
    name_filter = forms.CharField(max_length=100, required=False,label="Фільтрація по назві предмету ",label_suffix=": ", )

class GradeForm(forms.Form):
    grade = forms.IntegerField()
    course_group_pk = forms.IntegerField()
    button = forms.CharField(max_length=10, required=True)
   