from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    title = models.CharField(max_length=150)
    
    description = models.TextField()
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
        null=True,
        blank=True,
        default=None
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("REVIEW", "Review"),
            ("COMPLETED", "Completed")
        ],
        default="PENDING"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    deadline = models.DateTimeField(
        null=True,
        blank=True
    )
    
class SubTask(models.Model):
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
    )
    
    title = models.CharField(max_length=200)
    completed = models.BooleanField(
        default=False
    )


