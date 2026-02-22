"""
Profile models for user profiles and authentication
"""
from django.db import models
from django.contrib.auth.models import User
from bson import ObjectId


class Profile(models.Model):
    """User profile model with fitness tracking information"""
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    grade = models.CharField(max_length=10, blank=True, null=True)  # fitness grade/level
    team = models.CharField(max_length=255, blank=True, null=True)  # team association
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return self.name