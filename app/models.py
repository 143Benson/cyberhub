from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('internet', 'Internet'),
        ('printing', 'Printing'),
        ('government', 'Government'),
        ('financial', 'Financial'),
        ('education', 'Education'),
        ('business', 'Business'),
        ('tech', 'Tech Services'),
        ('travel', 'Travel'),
        ('entertainment', 'Entertainment'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def icon_class(self):
        return f"fa-{self.icon}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"