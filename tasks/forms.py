from django import forms
from .models import Tasks
from django.contrib.auth.models import User

class Taskform(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'completed', 'assigned_to']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)      
        self.parent = kwargs.pop('parent', None) 
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.all()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        qs = Tasks.objects.filter(title=title)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Task already exists")
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.parent:
            instance.parent = self.parent
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance