from django.db import models
from django.contrib.auth.models import User

class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    abstract = models.TextField()
    pdf = models.FileField(upload_to='papers/', blank=True)
    thumbnail = models.ImageField(upload_to='papers/thumbs/', blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='paper_applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paper_applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField(blank=True)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.paper.title}"