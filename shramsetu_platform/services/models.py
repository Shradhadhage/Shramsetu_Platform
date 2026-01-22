from django.db import models
from django.contrib.auth.models import User

# services/models.py
class Profile(models.Model):
    # This links the profile to a specific User account
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Account details
    role = models.CharField(
        max_length=20, 
        choices=[('customer', 'Customer'), ('worker', 'Worker')],
        default='customer'
    )
    
    # Extra details for the "Edit" page
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skill = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hired_jobs')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_jobs')
    title = models.CharField(max_length=200)
    # Fix: Allow these to be empty in the database
    description = models.TextField(null=True, blank=True) 
    budget = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    # ... other fields ...

class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hired_jobs')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_jobs')
    title = models.CharField(max_length=200)
    # Added null=True, blank=True to prevent "NOT NULL constraint failed"
    description = models.TextField(null=True, blank=True) 
    budget = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"