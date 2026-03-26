from django.db import models
from django.contrib.auth.models import User
class Tasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=True, blank=True      
    )

    def __str__(self):
        return self.title

class SubTask(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'title')

    def __str__(self):
        return self.title
