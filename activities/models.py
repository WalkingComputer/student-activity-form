from django.db import models

class Submission(models.Model):
    ACTIVITY_CHOICES = [
        ('industrial_visit', 'Industrial Visit'),
        ('tech_viva', 'Technology Viva Presentation'),
    ]

    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    section = models.CharField(max_length=20)
    choice = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    viva_topic = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

    class Meta:
        ordering = ['-created_at']
