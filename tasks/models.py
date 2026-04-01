from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=True,
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtasks'
    ) #subtask model
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'title')

    def __str__(self):
        return self.title

    @property
    def is_subtask(self):
        return self.parent is not None
        