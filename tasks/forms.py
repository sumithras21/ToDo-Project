from django import forms
from .models import Tasks, SubTask
from django.contrib.auth.models import User

class Taskform(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'completed', 'assigned_to']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.all()

        if user:
            self.fields['assigned_to'].queryset = User.objects.exclude(id=user.id)
            
    def clean_title(self):
        title = self.cleaned_data.get('title')
        qs = Tasks.objects.filter(title=title)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise forms.ValidationError("Task already exists")

        return title

class SubTaskform(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'completed']

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        qs = SubTask.objects.filter(title=title)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise forms.ValidationError("Subtask already exists")

        return title
