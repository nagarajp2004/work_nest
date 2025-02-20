from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES=[('pending','pending'),('In progress','In progress'),('Completed', 'Completed'),]

    PRIORITY_CHOICES=[('High','High'),('Medium','Medium'),('Low','Low'),]

    title=models.CharField(max_length=200)
    description=models.TextField()
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE)
    created_by=models.ForeignKey(User,related_name='created_tasks',on_delete=models.CASCADE)
    due_date=models.DateTimeField()
    priority=models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='Medium')
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
     return self.title


# Create your models here.
