from django.conf import settings
from django.db import models
from django.utils.text import slugify
from accounts.models import EmployerProfile
from django.urls import reverse
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Job(models.Model):
    EMPLOYMENT_CHOICES = (
        ('FT','Full-time'),
        ('PT','Part-time'),
        ('CT','Contract'),
        ('IN','Internship'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True, db_index=True)
    company = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_CHOICES, default='FT')
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-posted_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.company.company_name}")[:250]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} @ {self.company.company_name}"

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'pk': self.id, 'slug': self.slug})

class Application(models.Model):
    STATUS_CHOICES = (
        ('APPLIED','Applied'),
        ('SHORTLISTED','Shortlisted'),
        ('REJECTED','Rejected'),
        ('HIRED','Hired'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"

